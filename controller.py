from frame import Frame
from bot import Bot
from character import Character
from classifier import Classifier
import numpy as np
from configparser import  SafeConfigParser
import configparser
import pickle

# controller class, every subsystem is initialized, and passed down to the classes that need them here
# this enables the system to be highly modular, every component (classifier, bot, character) can be switched
class Controller:
    def __init__(self):
        # read config file and save values in variables
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.name = self.config.get("default", "botname")
        self.first_launch = self.config.getboolean("default", "firstlaunch")

        # initialize chat variables
        self.response = None
        self.log_message = []
        self.input_emotions = []
        self.input_topics = []
        self.response_confidence = None

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
        self.frame = Frame(self.name, self.bot, self.emotional_state, self.emotional_history)
        self.frame.register(self)
        self.frame.show()

        self.b = {"hello", "fiend"}
        self.output_file = open("picle.p", "wb")
        pickle.dump({"hi", "you"}, self.output_file)
        self.output_file.close()
        #self.k = pickle.load(open("picle.p", "rb"))
        #print(self.k)

        print("frame closed")
        self.save_data()

        if self.first_launch:
            self.config.set("default", "firstlaunch", "NO")
            with open("config.ini", "w") as f:
                self.config.write(f)

    # handles saving data when closing the program
    def save_data(self):
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

        self.response = self.response_package.get("response")
        self.response_confidence = self.response_package.get("response_confidence").__str__()
        self.input_emotions = self.response_package.get("input_emotions")
        self.input_topics = self.response_package.get("input_topics")




       # self.emotional_state = self.character.update_emotional_state(self.input_emotions)
        self. emotional_state = self.bot_state_package.get("emotional_state")
        #self.emotional_history = self.character.update_emotional_history(self.emotional_state)
        self.emotional_history = self.bot_state_package.get("emotional_history")





        self.log_message.extend(self.combine_lists("\nBot emotional state: ", self.input_emotions))
        # append log message
        self.log_message = self.combine_lists("Input emotion analysis: ", self.input_emotions)
        self.log_message.extend(self.combine_lists("\nInput keyword analysis: ", self.input_topics))
        self.log_message.append("\nBot response confidence:\nconfidence " + self.response_confidence)
        self.log_message.extend(self.combine_lists("\nBot emotional state: ", self.emotional_state))

        # test: numpy-arrays lassen sich genauso verwenden wie normale arrays
        self.emotional_state = np.array(self.emotional_state)

        # update widgets
        self.frame.update_chatout(user_message, self.response.__str__())
        self.frame.update_log(self.log_message)
        self.frame.update_diagrams(self.emotional_state, self.character.get_emotional_history())



    # combines to lists, eg: emotion names from one list and the respective values from another
    def combine_lists(self, title, list):
        self.a = [title]
        for item in range(0, 5):
            self.a.append(self.emotions[item] + ": " + list[item].__str__())
        return self.a


controller = Controller()
