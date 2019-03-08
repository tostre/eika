from frame import Frame
from bot import Bot
from character import Character
from classifier import Classifier
from character_manager import Character_Manager
import configparser
import pickle
import logging
from timeit import Timer


# TODO alles außer fear und anger scheint sich nicht zu ändern


# controller
# class, every subsystem is initialized, and passed down to the classes that need them here
# this enables the system to be highly modular, every component (classifier, bot, character) can be switched
class Controller:
    def __init__(self):
        # logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(name)s/%(levelname)s - - %(message)s', datefmt='%d.%m.%y %H:%M:%S')
        logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(name)s/%(levelname)s - - %(message)s', datefmt='%d.%m.%y %H:%M:%S')
        self.log = logging.getLogger("controller")
        self.log.info("program started")

        self.c_manager = Character_Manager("character_default")
        self.work = None
        # read config file and save values in variables
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.botname = self.config.get("default", "botname")

        # initialize chat variables
        self.response_package = None
        self.bot_state_package = None
        self.log_message = []

        # initialize emotional variables
        self.emotions = ["happiness", "sadness", "anger", "fear", "disgust"]
        self.topic_keywords = ["joy", "sadness", "anger", "fear", "disgust"]
        self.topic_keywords_pos_sentiment = ["positive_emotion", "optimism", "affection", "cheerfulness", "politeness", "love", "attractive"]
        self.topic_keywords_neg_sentiment = ["cold", "swearing_terms", "disappointment", "pain", "neglect", "suffering", "negative_emotion", "hate", "rage"]

        # create bot, responsible for generating answers and classifier, for analysing the input
        self.character = Character(self.emotions, "character_saved", self.config.getboolean("default", "firstlaunch"))
        print(self.character)
        self.classifier = Classifier(self.topic_keywords)
        self.bot = Bot(self.botname, self.character, self.classifier)

        # create frame and update widgets with initial values
        self.frame = Frame(self.botname, self.bot, self.character, self.bot.get_emotional_state(), self.bot.get_emotional_history())
        self.frame.register_subscriber(self)
        self.frame.show()

        # save all session data after the frame is closed
        self.save_session()
        logging.shutdown()

    def configure_logger(self):
        self.logger = logging.getLogger("controller")
        self.logger.setLevel(logging.INFO)

    def handle_intent(self, intent, input_message=None, character=None):
        if intent == "load_character":
            self.load_character(character)
            self.frame.update_diagrams(self.character.get_emotional_state(), self.character.get_emotional_history())
        elif intent == "get_response":
            if input_message and input_message != "":
                self.handle_input(input_message)
        elif intent == "retrain_bot":
            self.bot.train()
        elif intent == "reset_state":
            self.character.reset_bot()
            self.frame.update_diagrams(self.character.get_emotional_state(), self.character.get_emotional_history())


    # take user input, generate new data an update ui
    def handle_input(self, user_message):
        self.log.info("handle input")
        logging.info("input")
        # get new values based in response
        self.response_package, self.bot_state_package = self.bot.respond(user_message)

        # append log message
        self.log_message.clear()
        self.log_message.append("=== bot emotional state")
        self.log_message.append(self.bot_state_package.get("emotional_state").__str__())
        self.log_message.append("=== bot emotional history")
        self.log_message.append(self.bot_state_package.get("emotional_history").__str__())
        self.log_message.append("=== input message emotions")
        self.log_message.append(self.response_package.get("input_emotions").__str__())
        self.log_message.append("=== input topics")
        self.log_message.append(self.response_package.get("input_topics").__str__())
        self.log_message.append("=== response confidence")
        self.log_message.append(self.response_package.get("response_confidence").__str__())

        # update widgets
        self.frame.update_chat_out(user_message, self.response_package.get("response").__str__())
        # TODO: Die update-log Methode so umschreiben: Man kann beliebig viele Parameter übergeben (in einem Array oder einfachs so)
        # Die werden dann in der update_log-Methode mit einem Linebreak aneinander verkettet und gezeichnet
        # so muss man die nicht alle hier erst zu einem String zusammenfassen
        self.frame.update_log(self.log_message)
        self.frame.update_diagrams(self.bot_state_package.get("emotional_state"), self.bot_state_package.get("emotional_history"))

    def update_log(self, messages):
        self.log_output = []
        for item in messages:
            self.log_output.append(item.__str__())
        return self.log_output

    def load_character(self, file):
        self.character.load(file)

    # handles saving data when closing the program
    def save_session(self):
        # saves current character state
        self.character.save()

        # set the first launch variable to false
        self.config.set("default", "firstlaunch", "NO")
        # save new value in file
        with open("config.ini", "w") as f:
            self.config.write(f)

        self.log.info("character saved")


controller = Controller()

# for key, item in active_diagrams.items():
#    print(key)
#    print(item)
