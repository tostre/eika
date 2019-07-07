# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import nltk
import empath
import numpy
import random
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import webtext
from nltk.corpus import stopwords

class Classifier:
    def __init__(self, topic_keywords):
        self.lexicon = empath.Empath()
        self.keyword_analysis = []
        self.emotion_analysis = []
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
        self.emotion_analysis = []
        self.emotion_analysis = [round(random.uniform(0, 1), 2),
                                 round(random.uniform(0, 1), 2),
                                 round(random.uniform(0, 1), 2),
                                 round(random.uniform(0, 1), 2),
                                 round(random.uniform(0, 1), 2)]
        return self.emotion_analysis

    # returns a list of tokens
    def get_tokens_nltk(self, input):
        example_sentence = "The examples are all taken from real texts in the World English Corpus. We don't sit at our desks and make them up – we research the language and take the most typical uses and embed them in the entries. Users of MacmillanDictionary.com can be sure that the language they encounter here is up-to-date, accurate, and reflects the language as it is used in the 21st century. Mr. Smith said so."
        sentences = sent_tokenize(example_sentence)
        print(sentences.type())
        #input_data = numpy.zeros((sentences., 4))
        #print(input_data)


        # Eingabe in Sätze und Wörter tokeniseren

        words = word_tokenize(example_sentence)



        # There is also a corpus of stopwords, that is, high-frequency words like
        # the, to and also that we sometimes want to filter out of a document before
        # further processing. Stopwords usually have little lexical content, and their
        # presence in a text fails to distinguish it from other texts.
        stop_words = set(stopwords.words("english"))

        filtered_sentence = []

        for item in words:
            if item not in stop_words:
                filtered_sentence.append(item)

        print(sentences)
        print(words)
        pass