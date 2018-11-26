import chatterbot as cb
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import empath
import spacy


class newBot:
    # im Prinzip der Konstruktor, self ist die Instanz als Objekt (denke: this in Java)
    def __init__(self, name, character, categories):
        self.response = None
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
        # self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.set_trainer(ListTrainer)

        self.nlp = spacy.load("en")
        self.spacy_test()

    def spacy_test(self):
        # word tokenization
        self.doc = self.nlp("spacy is a cool tool")
        for token in self.doc:
            print(token)
            print(token.text)
        # make a list out of word tokens
        # make an entra of type token.text for every token in doc
        self.word_list = [token.text for token in self.doc]
        print(self.word_list)

        # sentence tokenization
        self.doc_file = self.nlp(open("example.txt").read())
        for num, sentence in enumerate(self.doc_file.sents):
            print(f"{num}: {sentence}")
        print(self.doc_file)

    def train(self):
        self.bot.train([
            "Hi, can I help you?",
            "Sure, I'd like to book a flight to Iceland.",
            "Your flight has been booked."
        ])
        # self.bot.train("chatterbot.corpus.english")
        return "Training complete"

    # returns chatbot response, with some additional data
    def respond(self, input):
        self.response = self.bot.get_response(input)
        self.response.add_extra_data("topics", self.analyze_topics(input))
        return self.response


    # analyzes and returns topics of the input using empath
    def analyze_topics(self, input):
        # returns topics as a list/set
        self.topicsSet = self.lexicon.analyze(input, normalize=True, categories=self.categories)
        self.topics = ["Input topics analysis",
                       "happiness: " + self.topicsSet["joy"].__str__(),
                       "sadness: " + self.topicsSet["sadness"].__str__(),
                       "anger: " + self.topicsSet["anger"].__str__(),
                       "fear: " + self.topicsSet["fear"].__str__(),
                       "disguist: " + self.topicsSet["disguist"].__str__()]
        return self.topics

    # analyzes and returns emotions of the input
    # muss hier noch ein richtiges tool finden
    # vlt den prof fragen
    def analyze_emotions(self):
        pass
