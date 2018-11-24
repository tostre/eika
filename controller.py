import frame
import bot
import character


class newController:
    def __init__(self, name):
        # intialize chat variables
        self.response = None
        self.logmessage = None

        # initialize character parameters
        self.h = set()
        self.s = set()
        self.a = set()
        self.f = set()
        self.d = set()
        self.character = character.newCharacter(
            {"trait": 0.3, "val": 0.3, "maxVal": 0.9, "actVal": 0.3},
            {"trait": 0.1, "val": 0.1, "maxVal": 0.7, "actVal": 0.2},
            {"trait": 0.2, "val": 0.2, "maxVal": 0.4, "actVal": 0.5},
            {"trait": 0.0, "val": 0.0, "maxVal": 0.5, "actVal": 0.7},
            {"trait": 0.1, "val": 0.1, "maxVal": 0.6, "actVal": 0.3}
        )
        self.categories = ["joy", "sadness", "anger", "fear", "disguist"]
        self.bot = bot.newBot(name, self.character, self.categories)
        self.bot.train()

        self.frame = frame.newFrame(name, self.bot)
        self.frame.register(self)
        self.frame.show()

    def handle_input(self, input):
        # get response statement from bot
        self.response = self.bot.respond(input)
        # analyze input for topics
        self.logmessage = self.bot.analyze_topics(input)
        # get confidence for generated response
        self.logmessage.append("\nresponse confidence: " + self.response.confidence.__str__())
        # update widgets
        self.frame.updateChatOut(input, self.response.__str__())
        self.frame.updateLog(self.logmessage)


controller = newController("EIKA")
