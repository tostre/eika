# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

class classifier:
    def __init__(self, emo_keyword_categories, pos_sentiment_keyword_categories, neg_sentiment_keyword_categories):
        self.emo_keyword_categories = emo_keyword_categories
        self.pos_sentiment_keyword_categories = pos_sentiment_keyword_categories
        self.neg_sentiment_keyword_categories = neg_sentiment_keyword_categories

emo_keyword_categories = {"joy", "sadness", "anger", "fear", "disguist"}
pos_sentiment_keyword_categories = {"positive_emotion", "optimism", "affection", "cheerfulness", "politeness", "love", "attractive"}
neg_sentiment_keyword_categories = {"cold", "swearing_terms", "disappointment", "pain", "neglect", "suffering", "negative_emotion", "hate", "rage"}