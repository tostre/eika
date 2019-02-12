import chatterbot as cb
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging


# this analyzes user inputs and generates a response
class Bot:
    def __init__(self, name, character, classifier):
        # this is so i dont get a minor error message every turn
        logger = logging.getLogger()
        logger.setLevel(logging.CRITICAL)
        # identity of the bot
        self.character = character
        self.classifier = classifier

        self.response = None
        self.response_package = {}
        self.bot_state_package = {}

        self.bot = cb.ChatBot(
            name,
            preprocessors=[
                'chatterbot.preprocessors.clean_whitespace'
            ]
        )

        self.train()

    def train(self):
        trainer = ChatterBotCorpusTrainer(self.bot)
        trainer.train("chatterbot.corpus.english.conversations")
        return "Training complete"

    # returns chatbot response, with some additional data
    def respond(self, user_message):
        self.response = self.bot.get_response(user_message)

        self.response_package = {
            "response": self.response,
            "response_confidence": self.response.confidence,
            "input_emotions": self.classifier.get_emotions(user_message),
            "input_topics": self.classifier.get_topics(user_message),
        }

        self.emotional_state, self.emotional_history = self.character.update_emotional_state(self.response_package.get("input_emotions"))

        self.bot_state_package = {
            "emotional_state": self.emotional_state,
            "emotional_history": self.emotional_history
        }
        return self.response_package, self.bot_state_package

    def get_packages(self):
        return self.response_package, self.bot_state_package

    def get_response_package(self):
        return self.response_package

    def get_bot_state_package(self):
        return self.bot_state_package

    def get_emotional_state(self):
        return self.character.get_emotional_state()

    def get_emotional_history(self):
        return self.character.get_emotional_history()

    def get_character_package(self):
        return self.character.get_character_package()
