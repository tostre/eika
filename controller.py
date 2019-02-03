from frame import Frame
from bot import Bot
from character import Character
from classifier import Classifier
import numpy as np


# controller class, every subsystem is initialized, and passed down to the classes that need them here
# this enables the system to be highly modular, every component (classifier, bot, character) can be switched
class Controller:
    def __init__(self):
        # intialize chat variables
        self.response = None
        self.log_message = []
        self.input_emotions = []
        self.input_topics = []
        self.response_confidence = None

        # initialize emotional variables
        self.emotions = ["happiness", "sadness", "anger", "fear", "disgust"]
        self.emo_keyword_categories = ["joy", "sadness", "anger", "fear", "disgust"]
        self.pos_sentiment_keyword_categories = ["positive_emotion", "optimism", "affection", "cheerfulness", "politeness", "love", "attractive"]
        self.neg_sentiment_keyword_categories = ["cold", "swearing_terms", "disappointment", "pain", "neglect", "suffering", "negative_emotion", "hate", "rage"]

        # initialize character, val = currentValue
        self.trait_values = [0.100, 0.100, 0.100, 0.100, 0.100]
        self.max_values = [0.900, 0.900, 0.900, 0.900, 0.900]
        self.character = Character(self.emotions, self.trait_values, self.max_values)
        self.emotional_state = self.character.get_emotional_state()
        self.emotional_history = self.character.get_emotional_history()

        # create bot, responsoble for generating answers and classfifer, for analysing the input
        self.name = "ChotterBotter"
        self.classifier = Classifier()
        self.bot = Bot(self.name, self.character, self.classifier)
        self.bot.train()

        # create frame and update widgets with initial values
        self.frame = Frame(self.name, self.bot, self.emotional_state, self.emotional_history)
        self.frame.register(self)
        self.frame.show()

    # take user input, generate new data an update ui
    def handle_input(self, user_input):
        # get new values based in response
        self.response = self.bot.respond(user_input)
        self.input_emotions = self.classifier.get_emotions(user_input)
        self.input_topics = self.classifier.get_topics(user_input, self.emo_keyword_categories)
        self.response_confidence = self.response.confidence.__str__()
        self.emotional_state = self.character.update_emotional_state(self.input_emotions)
        self.emotional_history = self.character.update_emotional_history(self.emotional_state)
        self.log_message.extend(self.combine_lists("\nBot emotional state: ", self.input_emotions))

        # append log message
        self.log_message = self.combine_lists("Input emotion analysis: ", self.input_emotions)
        self.log_message.extend(self.combine_lists("\nInput keyword analysis: ", self.input_topics))
        self.log_message.append("\nBot response confidence:\nconfidence " + self.response_confidence)
        self.log_message.extend(self.combine_lists("\nBot emotional state: ", self.emotional_state))

        # test: numpy-arrays lassen sich genauso verwenden wie normale arrays
        self.emotional_state = np.array(self.emotional_state)

        # update widgets
        self.frame.update_chatout(user_input, self.response.__str__())
        self.frame.update_log(self.log_message)
        self.frame.update_diagrams(self.emotional_state, self.character.get_emotional_history())

        #self.character.update_s(self.input_emotions)

    # combines to lists, eg: emotion names from one list and the respective values from another
    def combine_lists(self, title, list):
        self.a = [title]
        for item in range(0, 5):
            self.a.append(self.emotions[item] + ": " + list[item].__str__())
        return self.a


controller = Controller()
