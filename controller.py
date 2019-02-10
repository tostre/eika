from frame import Frame
from bot import Bot
from character import Character
from classifier import Classifier
import configparser

# TODO emotional history scheint sich nicht richtig zu updaten
# TODO alles außer fear und anger scheint sich nicht zu ändern

# controller
# class, every subsystem is initialized, and passed down to the classes that need them here
# this enables the system to be highly modular, every component (classifier, bot, character) can be switched
class Controller:
    def __init__(self):
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
        self.character = Character(self.emotions, self.config.getboolean("default", "firstlaunch"))
        self.classifier = Classifier(self.topic_keywords)
        self.bot = Bot(self.botname, self.character, self.classifier)

        # create frame and update widgets with initial values
        self.frame = Frame(self.botname, self.bot, self.character, self.bot.get_emotional_state(), self.bot.get_emotional_history())
        self.frame.register(self)
        self.frame.show()

        # save all session data after the frame is closed
        self.save()

    # handles saving data when closing the program
    def save(self):
        # saves current character state
        self.character.save()
        
        # set the first launch variable to false
        self.config.set("default", "firstlaunch", "NO")
        # save new value in file
        with open("config.ini", "w") as f:
            self.config.write(f)

    # take user input, generate new data an update ui
    def handle_input(self, user_message):
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
        self.frame.update_log(self.log_message)
        self.frame.update_diagrams(self.bot_state_package.get("emotional_state"), self.bot_state_package.get("emotional_history"))


controller = Controller()
