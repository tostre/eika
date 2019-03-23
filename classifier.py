# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

import empath
import random

class Classifier:
    def __init__(self, topic_keywords):
        self.lexicon = empath.Empath()
        self.keyword_analysis = []
        self.input_emotions = np.zeros(5)
        self.topic_keywords = topic_keywords

    # analyzes and returns topics of the input using empath
    def get_topics(self, user_message):
        self.keyword_analysis = []
        self.topics_set = self.lexicon.analyze(user_message, categories=self.topic_keywords, normalize=True)
        for item in self.topic_keywords:
            self.keyword_analysis.append(round(self.topics_set[item], 2).__str__())
        return self.keyword_analysis

    # analyzses and returns general sentiment of the input
    def get_sentiment(self, input):
        pass

    # atm returns a list of random generated emotion values
    def get_emotions(self, input):
        self.input_emotions = np.round(np.random.rand(5), 3)
        return self.input_emotions
