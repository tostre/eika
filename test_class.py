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
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import webtext
from nltk.corpus import wordnet
import spacy

class Test:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmer = WordNetLemmatizer()

        self.example_sentence = "The examples are all taken from real texts in the World English Corpus. We don't sit at our desks and make them up – we research the language and take the most typical uses and embed them in the entries. Users of MacmillanDictionary.com can be sure that the language they encounter here is up-to-date, accurate, and reflects the language as it is used in the 21st century. Mr. Smith said so. Python. Pythoner"

        #self.get_tokens_nltk(self.example_sentence)
        self.token_list = []
        self.filtered_token_list = []
        self.stemmed_token_list = []
        self.pos_token_list = []
        self.lemmed_token_list = []

        self.stop_words = set(stopwords.words("english"))

        self.input_sentences = sent_tokenize(self.example_sentence)

        for input_sentence in self.input_sentences:
            #self.tokenize(input_sentence)
            pass

        self.space(input_sentence[0])
        pass

    def space(self, input_sentence):
        doc = nlp(input_sentence)
        for token in doc:
            print(token.text)
        pass

    def tokenize (self, input_sentence):
        self.sentence_data = {
            "sentence": input_sentence,
            "tokens": [],
            "pos_tags": [],
            "lemmed_tokens": []
        }

        # Tokenize the input sentence
        self.token_list = word_tokenize(input_sentence)
        # Delete stop words from tokens (words that have little to no meaning)
        for word in self.token_list:
            if word not in self.stop_words:
                self.filtered_token_list.append(word)
        # Stem tokens in filtered token list
        for index, word in enumerate(self.filtered_token_list):
            self.stemmed_token_list.append(self.stemmer.stem(word))
        # Generate pos-Tags for tokens
        self.pos_token_list = nltk.pos_tag(self.stemmed_token_list)

        # create lemmas from stems
        for tupel in self.sentence_data["pos_tags"]:
            self.lemmed_token_list.append(self.lemmer.lemmatize(tupel[0], self.get_wordnet_tag(tupel[1])))
            print(self.lemmer.lemmatize(tupel[0], self.get_wordnet_tag(tupel[1])))



        # Save tokenized and stemmes list
        self.sentence_data["tokens"] = self.stemmed_token_list.copy()
        self.sentence_data["pos_tags"] = self.pos_token_list.copy()
        self.sentence_data["lemmed_tokens"] = self.lemmed_token_list.copy()

        self.filtered_token_list.clear()
        self.stemmed_token_list.clear()
        self.pos_token_list.clear()
        self.lemmed_token_list.clear()

        print(self.sentence_data["tokens"])
        print(self.sentence_data["pos_tags"])
        print(self.sentence_data["lemmed_tokens"])
        print("\n")

    # converts treebank-pos-tags to wordnet-pos-tag
    def get_wordnet_tag(self, treebank_tag):
        print(treebank_tag)
        if treebank_tag.startswith('N'):
            return "n"
        elif treebank_tag.startswith('J'):
            return "a"
        elif treebank_tag.startswith('R'):
            return "r"
        elif treebank_tag.startswith('V'):
            return "v"
        else:
            return "n"

    # returns a list of tokens
    def get_tokens_nltk(self, input):
        self.text_data = []
        self.token_list = []
        self.filtered_token_list = []

        self.sentences = sent_tokenize(self.example_sentence)


        # save sentence and tokens in list
        for entry in self.sentences:
            self.l = [entry, word_tokenize(entry)]
            self.text_data.append(self.l)

        # filter token list for stop words (words that hold no important information)
        for entry in self.text_data:
            self.token_list = entry[1]
            for word in self.token_list:
                if word not in self.stop_words:
                    self.filtered_token_list.append(word)
            entry[1] = self.filtered_token_list.copy()
            self.filtered_token_list.clear()

        # stem tokens
        for entry in self.text_data:
            self.token_list = entry[1]
            print(self.token_list)
            for index, word in enumerate(self.token_list):
                print(word)
                print(self.stemmer.stem(word))
                self.stemmer.stem(word)
                self.token_list[index] = self.stemmer.stem(word)




        pass