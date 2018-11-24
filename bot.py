import chatterbot as cb
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import empath

class newBot:
    # im Prinzip der Konstruktor, self ist die Instanz als Objekt (denke: this in Java)
    def __init__(self, name, character, categories):
        self.lexicon = empath.Empath()
        self.name = name
        self.character = character
        self.categories = categories

        self.bot = cb.ChatBot(
            name,
            preprocessors=[
                'chatterbot.preprocessors.clean_whitespace'
            ]
        )
        #self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.set_trainer(ListTrainer)

    def train(self):
        self.bot.train([
            "Hi, can I help you?",
            "Sure, I'd like to book a flight to Iceland.",
            "Your flight has been booked."
        ])
        #self.bot.train("chatterbot.corpus.english")
        return "Training complete"

    # returns chatbot response
    def respond(self, input):
        return self.bot.get_response(input).__str__()

    # analyzes and returns topics of the input using empath
    def getTopics(self, input):
        # returns topics as a list/set
        self.topicsSet = self.lexicon.analyze(input, normalize=True, categories=self.categories)
        self.topics= ["Input topics analysis",
                          "happiness: " + self.topicsSet["joy"].__str__(),
                          "sadness: " + self.topicsSet["sadness"].__str__(),
                          "anger: " + self.topicsSet["anger"].__str__(),
                          "fear: " + self.topicsSet["fear"].__str__(),
                          "disguist: " + self.topicsSet["disguist"].__str__()]
        return self.topics

    # analyzes and returns emotions of the input
    # muss hier noch ein richtiges tool finden
    # vlt den prof fragen
    def getEmotions(self):
        pass





