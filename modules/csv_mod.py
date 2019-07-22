import spacy
import pandas


class Csv_tool:
    def __init__(self):
        pandas.options.mode.chained_assignment = None  # default='warn'
        self.nlp = spacy.load("en")
        self.doc = None
        self.spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
        self.num_sentences = []
        self.lemmas = []
        self.pos = []
        self.shapes = []
        self.num_ents = []

        self.dataset = None
        self.drop_rows = None
        self.clean_rows = None
        self.emotions = ["happiness", "sadness", "anger", "fear", "disgust"]
        self.datasets = [["test", ","], ["crowdflower", ","], ["emoint", "\t"],
                         ["emotion_classification", ","],
                         ["isear", "\t"], ["meld", ","], ["tec", "\t"]]
        # self.datasets = [["crowdflower", ","]]
        self.datasets = [["test", ","]]

        self.cleanup_datasets()
        self.discern_features()

    # Removes unwanted emotion tags, forbidden strings and every delimiter but ","
    def cleanup_datasets(self):
        for dataset in self.datasets:
            print("cleaning up dataset", dataset[0])
            # Read the dataset
            self.dataset = pandas.read_csv("corpora/" + dataset[0] + ".csv", delimiter=dataset[1])

            # Choose only the rows annotated with 1 of the 5 emotions
            print("... removing unwanted affect tags")
            self.clean_rows = self.dataset.loc[(self.dataset["affect"] == "happiness") |
                                               (self.dataset["affect"] == "sadness") |
                                               (self.dataset["affect"] == "anger") |
                                               (self.dataset["affect"] == "fear") |
                                               (self.dataset["affect"] == "disgust")]
            # Reset the index numbers for the rows
            self.clean_rows.reset_index(inplace=True, drop=True)

            # Delete all rows that contain links or @-mentions
            print("... removing links and mentions")
            self.drop_rows = []
            for index, row in self.clean_rows.iterrows():
                if row["text"].__contains__("http") \
                        or row["text"].__contains__("@") \
                        or row["text"].__contains__("#"):
                    self.drop_rows.append(False)
                else:
                    self.drop_rows.append(True)
                    # Replace some strings
                    self.clean_rows.iloc[index, 1] = self.clean_rows.iloc[index, 1] \
                        .replace("&quot", "\"") \
                        .replace("&amp", "&") \
                        .replace("&lt", "<") \
                        .replace("&gt", ">")

            self.drop_rows = pandas.Series(self.drop_rows)
            # Choose only the rows that don't contain links or mentions
            self.clean_rows = self.clean_rows[self.drop_rows]

            # Save these datasets as a cleaned up corpus with delimiter ","
            self.clean_rows.reset_index(inplace=True, drop=True)
            self.clean_rows.to_csv("corpora/" + dataset[0] + "_clean.csv", sep=",", index=False)
            print("... done\n")

    # analyzes linguistic features of the csv and saves them in file
    def discern_features(self):
        for dataset in self.datasets:
            print("searching for linguistic features in", dataset[0])
            # Read the dataset
            self.dataset = pandas.read_csv("corpora/" + dataset[0] + "_clean.csv", delimiter=dataset[1])
            self.dataset = self.dataset.astype('object')

            # for every entry in the dataset
            for index, row in self.dataset.iterrows():
                self.doc = self.nlp(row["text"])
                self.num_sentences = len(list(self.doc.sents))
                # create lists for pos, lemma etc, and insert them into overall lemma/pos-lists
                self.lemmas.append([(token.lemma_) for token in self.doc if not token.is_stop])
                self.pos.append([(token.pos_) for token in self.doc if not token.is_stop])
                self.shapes.append([(token.shape_) for token in self.doc if not token.is_stop])
                self.num_ents.append(len(self.doc.ents))

            # Write the linguiistic lists into the dataFrame
            print("saving features to the dataframe")
            self.dataset["num_sentences"] = self.num_sentences
            self.dataset["lemmas"] = self.lemmas
            self.dataset["pos"] = self.pos
            self.dataset["shapes"] = self.shapes
            self.dataset["num_ents"] = self.num_ents

            # save the dataset to the file system
            self.dataset.to_csv("corpora/" + dataset[0] + "_clean.csv", sep=",", index=False)
            print("... done\n")

    # @todo
    # vlt kann ich diese datensätze nicht nehmen:
    # isear: beschreibungen von vorfällen
    # crowdflower: sind hashtags drin
    # emoint (hashtags)
    # meld (sind keine chatnachrichten, sondern sauber abgetippte tv-dialoge)
    # tec (hashtags, außerdem spanische zeilen)

    # features: satzzeichen


cleaner = Csv_tool()
