from frame import Frame
from bot import Bot
from character import Character
from classifier import Classifier
from character_manager import Character_Manager
import configparser
import logging


# controller
# class, every subsystem is initialized, and passed down to the classes that need them here
# this enables the system to be highly modular, every component (classifier, bot, character) can be switched
class Controller:
    def __init__(self):

        cm = Character_Manager("character_default")
        cm = Character_Manager("character_stable")
        cm = Character_Manager("character_empathetic")
        cm = Character_Manager("character_irascible")

        # set up logging
        logging.basicConfig(level=logging.INFO, filename='logs/app.log', filemode="w", format='%(asctime)s %(name)s/%(levelname)s - - %(message)s', datefmt='%d.%m.%y %H:%M:%S')
        self.logger = logging.getLogger("controller")
        self.logger.setLevel(logging.INFO)

        # read config file and save values in variables
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.botname = self.config.get("default", "botname")
        self.username = self.config.get("default", "username")

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
        self.character = Character(self.emotions, self.config.getboolean("default", "firstlaunch"))
        self.classifier = Classifier(self.topic_keywords)
        self.bot = Bot(self.botname, self.character, self.classifier)

        # create frame and update widgets with initial values
        self.frame = Frame(self.botname, self.username, self.character.get_emotional_state(), self.character.get_emotional_history())
        self.frame.register_subscriber(self)
        self.frame.show()

        # save all session data after the frame is closed
        self.save_session()
        logging.shutdown()

    # takes the users intent (per gui interaction) and starts the corresponding methods
    def handle_intent(self, intent, input_message=None, character=None):
        print("intent", intent)
        if intent == "load_character":
            self.character.load(character)
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
        # get new values based in response
        self.response_package, self.bot_state_package = self.bot.respond(user_message)
        # update gui
        self.frame.update_chat_out(user_message, self.response_package.get("response").__str__())
        self.frame.update_log([self.bot_state_package, self.response_package])
        self.frame.update_diagrams(self.bot_state_package.get("emotional_state"), self.bot_state_package.get("emotional_history"))

    # handles saving data when closing the program
    def save_session(self):
        # saves current character state
        self.character.save()

        # set the first launch variable to false
        self.config.set("default", "firstlaunch", "NO")
        # save new value in file
        with open("config.ini", "w") as f:
            self.config.write(f)


controller = Controller()
