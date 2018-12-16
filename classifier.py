# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

import empath
import random

class Classifier:
    def __init__(self):
        self.lexicon = empath.Empath()
        self.keyword_analysis = []
        self.emotion_analysis = []

    # analyzes and returns topics of the input using empath
    def get_topics(self, input, keyword_categories):
        self.keyword_analysis = []
        self.topics_set = self.lexicon.analyze(input, categories=keyword_categories, normalize=True)
        for item in keyword_categories:
            self.keyword_analysis.append(round(self.topics_set[item], 2).__str__())
        return self.keyword_analysis

    # analyzses and returns general sentiment of the input
    def get_sentiment(self, input):
        pass

    # atm returns a list of random generated emotion values
    def get_emotions(self, input):
        self.emotion_analysis = []
        self.emotion_analysis = [round(random.uniform(0, 1), 2),
                                 round(random.uniform(0, 1), 2),
                                 round(random.uniform(0, 1), 2),
                                 round(random.uniform(0, 1), 2),
                                 round(random.uniform(0, 1), 2)]
        return self.emotion_analysis
