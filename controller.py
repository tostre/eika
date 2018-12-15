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

        # list to build output strings, all lists are in this order
        self.emotion_titles = ["happiness", "sadness", "anger", "fear", "disgust"]

        # initialize character, val = currentValue, act = activationValue
        self.trait_values = [0.42, 0.13, 0.24, 0.00, 0.10]
        self.max_values = [0.9, 0.7, 0.4, 0.5, 0.6]
        self.act_values = [0.3, 0.2, 0.5, 0.7, 0.3]
        self.character = Character(self.trait_values, self.max_values, self.act_values)
        self.emotional_state = self.character.get_emotional_state()

        # create classifier topic keyword categories, classifier anlyzes inputs for these topics, emotions etc
        self.emo_keyword_categories = ["joy", "sadness", "anger", "fear", "disgust"]
        self.pos_sentiment_keyword_categories = ["positive_emotion", "optimism", "affection", "cheerfulness", "politeness", "love", "attractive"]
        self.neg_sentiment_keyword_categories = ["cold", "swearing_terms", "disappointment", "pain", "neglect", "suffering", "negative_emotion", "hate", "rage"]
        self.classifier = Classifier()

        # create bot, responsoble for generating answers
        self.bot = Bot(name)
        self.bot.train()

        # create frame
        self.frame = Frame(name, self.bot, self.emotion_titles, self.emotional_state)
        self.frame.register(self)
        self.frame.show()

    def handle_input(self, input):
        # generates a response
        self.response = self.bot.respond(input)
        # analyse emotions in input
        self.input_emotions = self.classifier.get_emotions(input)
        # analyses keywords for topics
        self.input_topics = self.classifier.get_topics(input, self.emo_keyword_categories)
        # append output confidence of answer
        self.response_confidence = self.response.confidence.__str__()
        # generate new emotional state of the character of the bot
        self.character.up(self.input_emotions)

        # get character state
        #self.character.update_emotional_state(self.input_emotions)
        #self.character.up(self.emotional_state)

        self.log_message.extend(self.combine_lists("\nBot emotional state: ", self.input_emotions))


        # append log message
        self.log_message = self.combine_lists("Input emotion analysis: ", self.input_emotions)
        self.log_message.extend(self.combine_lists("\nInput keyword analysis: ", self.input_topics))
        self.log_message.append("\nBot response confidence: " + self.response_confidence)

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
