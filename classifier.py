# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

import empath

class Classifier:
    def __init__(self):
        self.lexicon = empath.Empath()

    # analyzes and returns topics of the input using empath
    def get_topics(self, input, keyword_categories):
        self.topics_set = self.lexicon.analyze(input, categories=keyword_categories, normalize=True)
        self.topics_output = ["Input analysis:"]
        for item in keyword_categories:
            self.topics_output.append(item +": " + self.topics_set[item].__str__())
        print("topics out: ")
        print(self.topics_output)
        return self.topics_output

    # analyzses and returns general sentiment of the input
    def get_sentiment(self, input):
        pass

    # analyzes and returns emotions of the input
    # muss hier noch ein richtiges tool finden
    # vlt den prof fragen
    def get_emotions(self, input):
        pass

