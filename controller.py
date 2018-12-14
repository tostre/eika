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
        self.log_message = None

        # list to build output strings
        self.emotion_titles = ["happiness", "sadness", "anger", "fear", "disgust"]


        # initialize character, val = currentValue, act = activationValue
        self.trait_values = {"happiness": 0.3, "sadness": 0.1, "anger": 0.2, "fear": 0.0, "disgust": 0.1}
        self.max_values = {"happiness": 0.9, "sadness": 0.7, "anger": 0.4, "fear": 0.5, "disgust": 0.6}
        self.act_values = {"happiness": 0.3, "sadness": 0.2, "anger": 0.5, "fear": 0.7, "disgust": 0.3}
        self.character = Character(self.trait_values, self.max_values, self.act_values)

        # create classifier topic keyword categories, classifier anlyzes inputs for these topics, emotions etc
        self.emo_keyword_categories = ["joy", "sadness", "anger", "fear", "disgust"]
        self.pos_sentiment_keyword_categories = ["positive_emotion", "optimism", "affection", "cheerfulness", "politeness", "love", "attractive"]
        self.neg_sentiment_keyword_categories = ["cold", "swearing_terms", "disappointment", "pain", "neglect", "suffering", "negative_emotion", "hate", "rage"]
        self.classifier = Classifier()

        # create bot, responsoble for generating answers
        self.bot = Bot(name)
        self.bot.train()

        # create frame
        self.frame = Frame(name, self.bot)
        self.frame.register(self)
        self.frame.show()

        self.character.function("sigmoid", 2)

    def handle_input(self, input):
        # generates a response
        self.response = self.bot.respond(input)
        # analyse emotions in input
        self.log_message = self.combine_lists("Input emotion analysis: ", self.classifier.get_emotions(input))
        # analyses keywords for topics
        self.log_message.extend(self.combine_lists("\nInput keyword analysis: ", self.classifier.get_topics(input, self.emo_keyword_categories)))
        # append output confidence of answer
        self.log_message.append("\nBot response confidence: " + self.response.confidence.__str__())
        # get character state
        self.log_message.extend(self.combine_lists("\nBot emotional state: ", self.character.get_emotional_state()))
        # update widgets
        self.frame.updateChatOut(input, self.response.__str__())
        self.frame.updateLog(self.log_message)

    # combines to lists, eg: emotion names from one list and the respective values from another
    def combine_lists(self, title, list):
        self.a = [title]
        for item in range(0, 5):
            self.a.append(self.emotion_titles[item] + ": " + list[item].__str__())
        print(self.a)

        return self.a


# ein tf- oder pytrch-model ist egentlich die gewichte in dem neuronalen netz

controller = Controller("bot")