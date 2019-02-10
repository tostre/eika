from frame import Frame
from bot import Bot
from character import Character
from classifier import Classifier
import configparser

# controller
# class, every subsystem is initialized, and passed down to the classes that need them here
# this enables the system to be highly modular, every component (classifier, bot, character) can be switched
class Controller:
    def __init__(self):
        # read config file and save values in variables
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.name = self.config.get("default", "botname")
        self.first_launch = self.config.getboolean("default", "firstlaunch")

        # initialize chat variables
        self.response_package = None
        self.bot_state_package = None
        self.log_message = []
        self.input_emotions = []
        self.input_topics = []

        # initialize emotional variables
        self.emotions = ["happiness", "sadness", "anger", "fear", "disgust"]
        self.topic_keywords = ["joy", "sadness", "anger", "fear", "disgust"]
        self.topic_keywords_pos_sentiment = ["positive_emotion", "optimism", "affection", "cheerfulness", "politeness", "love", "attractive"]
        self.topic_keywords_neg_sentiment = ["cold", "swearing_terms", "disappointment", "pain", "neglect", "suffering", "negative_emotion", "hate", "rage"]

        # initialize character, val = currentValue
        self.character = Character(self.emotions, self.first_launch)
        self.emotional_state = self.character.get_emotional_state()
        self.emotional_history = self.character.get_emotional_history()

        # create bot, responsible for generating answers and classififer, for analysing the input
        self.classifier = Classifier(self.topic_keywords)
        self.bot = Bot(self.name, self.character, self.classifier)
        self.bot.train()

        # create frame and update widgets with initial values
        self.frame = Frame(self.name, self.bot, self.character, self.emotional_state, self.emotional_history)
        self.frame.register(self)
        self.frame.show()

        # save all session data
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

        self.input_emotions = self.response_package.get("input_emotions")
        self.input_topics = self.response_package.get("input_topics")

        self.emotional_state = self.bot_state_package.get("emotional_state")
        self.emotional_history = self.bot_state_package.get("emotional_history")

        # append log message
        self.log_message.clear()
        self.log_message.append("input message emotions")
        self.log_message.append(self.input_emotions.__str__())
        self.log_message.append("input topics")
        self.log_message.append(self.input_topics.__str__())
        self.log_message.append("response confidence")
        self.log_message.append(self.response_package.get("response_confidence").__str__())

        # update widgets
        self.frame.update_chatout(user_message, self.response_package.get("response").__str__())
        self.frame.update_log(self.log_message)
        self.frame.update_diagrams(self.emotional_state, self.emotional_history)


controller = Controller()
