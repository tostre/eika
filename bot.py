import chatterbot as cb

class newBot:
    # im Prinzip der Konstruktor, self ist die Instanz als Objekt (denke: this in Java)
    def __init__(self, name, character):
        self.name = name
        self.character = character
        self.bot = cb.ChatBot(
            'EIKA',
            trainer='chatterbot.trainers.ListTrainer'
        )

    def train(self):
        self.bot.train([
            "Hi, can I help you?",
            "Sure, I'd like to book a flight to Iceland.",
            "Your flight has been booked."
        ])
        print("Training complete")
        return "Training complete"

    def respondWithStatement(self, input):
        self.output = str(self.bot.get_response(input))
        print("input: " + input)
        print("output: " + self.output)
        return self.output

    def respond(self, input):
        self.output = self.bot.get_response(input).__str__()
        print("input 'text': " + input)
        print("output 'text': " + self.output)
        return self.output
