import chatterbot as cb
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer


# this class only generates outputs for a given user input. Based on the chatterbot library
class Bot:
    # im Prinzip der Konstruktor, self ist die Instanz als Objekt (denke: this in Java)
    def __init__(self, name):
        self.response = None
        self.name = name

        self.bot = cb.ChatBot(
            name,
            preprocessors=[
                'chatterbot.preprocessors.clean_whitespace'
            ]
        )
        # self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.set_trainer(ListTrainer)

    def train(self):
        self.bot.train([
            "Hi, can I help you?",
            "Sure, I'd like to book a flight to Iceland.",
            "Your flight has been booked."
        ])
        # self.bot.train("chatterbot.corpus.english")
        print("bot trained")
        return "Training complete"

    # returns chatbot response, with some additional data
    def respond(self, input):
        self.response = self.bot.get_response(input)
        # self.response.add_extra_data("topics", self.classifier.get_topics(input))
        return self.response
