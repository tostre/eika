from frame import Frame
from bot import Bot
from character import Character
from classifier import Classifier


# controller class, every subsystem is initialized and called here
# this enables the system to be highly modular, every component (classifier, bot, character) can be switched
class Controller:
    def __init__(self, name):
        # intialize chat variables
        self.response = None
        self.log_message = []
        self.input_emotions = []
        self.input_topics = []
        self.response_confidence = None

        # initialize emotional variables
        self.emotion_titles = ["happiness", "sadness", "anger", "fear", "disgust"]
        self.emo_keyword_categories = ["joy", "sadness", "anger", "fear", "disgust"]
        self.pos_sentiment_keyword_categories = ["positive_emotion", "optimism", "affection", "cheerfulness", "politeness", "love", "attractive"]
        self.neg_sentiment_keyword_categories = ["cold", "swearing_terms", "disappointment", "pain", "neglect", "suffering", "negative_emotion", "hate", "rage"]

        # initialize character, val = currentValue, act = activationValue
        self.trait_values = [0.42, 0.13, 0.24, 0.02, 0.10]
        self.max_values = [0.92, 0.70, 0.44, 0.57, 0.61]
        self.act_values = [0.21, 0.12, 0.30, 0.05, 0.10]
        self.character = Character(self.trait_values, self.max_values, self.act_values)
        self.emotional_state = self.character.get_emotional_state()

        # create bot, responsoble for generating answers and classfifer, for analysing the input
        self.bot = Bot(name)
        self.bot.train()
        self.classifier = Classifier()

        # create frame
        self.frame = Frame(name, self.bot, self.emotion_titles, self.emotional_state)
        self.frame.register(self)
        self.frame.show()

    # take user input, generate new data an update ui
    def handle_input(self, input):
        # get new values based in response
        self.response = self.bot.respond(input)
        self.input_emotions = self.classifier.get_emotions(input)
        self.input_topics = self.classifier.get_topics(input, self.emo_keyword_categories)
        self.response_confidence = self.response.confidence.__str__()
        self.emotional_state = self.character.update_emotional_state(self.input_emotions)
        self.log_message.extend(self.combine_lists("\nBot emotional state: ", self.input_emotions))

        # append log message
        self.log_message = self.combine_lists("Input emotion analysis: ", self.input_emotions)
        self.log_message.extend(self.combine_lists("\nInput keyword analysis: ", self.input_topics))
        self.log_message.append("\nBot response confidence:\nconfidence " + self.response_confidence)
        self.log_message.extend(self.combine_lists("\nBot emotional state: ", self.emotional_state))

        # update widgets
        self.frame.updateChatOut(input, self.response.__str__())
        self.frame.updateLog(self.log_message)

    # combines to lists, eg: emotion names from one list and the respective values from another
    def combine_lists(self, title, list):
        self.a = [title]
        for item in range(0, 5):
            self.a.append(self.emotion_titles[item] + ": " + list[item].__str__())
        return self.a


# ein tf- oder pytrch-model ist egentlich die gewichte in dem neuronalen netz

controller = Controller("bot")
