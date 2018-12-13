from frame import Frame
from bot import Bot
from character import Character
from classifier import Classifier

# controller class, every subsystem is initialized and called here
# this enables the system to be highly modular, every component (classifier, bot, character) can be switched
class newController:
    def __init__(self, name):
        # intialize chat variables
        self.response = None
        self.log_message = None

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
        #self.bot = bot.Bot(name, self.character, self.classifier)
        self.bot = Bot(name)
        self.bot.train()

        # create frame
        self.frame = Frame(name, self.bot)
        self.frame.register(self)
        self.frame.show()

    def handle_input(self, input):
        # generates response and analyzes it for topics/emotions etc
        self.response = self.bot.respond(input)
        self.log_message = self.classifier.get_topics(input, self.emo_keyword_categories)
        # get character state
        self.log_message.extend(self.character.get_emotional_state())
        # display output message date
        self.log_message.append("\nResponse data:")
        self.log_message.append("response confidence: " + self.response.confidence.__str__())
        # update widgets
        self.frame.updateChatOut(input, self.response.__str__())
        self.frame.updateLog(self.log_message)

# ein tf- oder pytrch-model ist egentlich die gewichte in dem neuronalen netz

controller = newController("bot")
