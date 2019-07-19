import csv
import pandas


class Cleaner:
    def __init__(self):
        self.csv_dataset = None
        self.drop_rows = None
        self.clean_rows = None
        self.emotions = ["happiness", "sadness", "anger", "fear", "disgust"]
        self.datasets = [["crowdflower", ","], ["emoint", "\t"],
                         ["emotion_classification", ","],
                         ["isear", "\t"], ["meld", ","], ["tec", "\t"]]
        #self.datasets = [["crowdflower", ","]]

        self.cleanup_datasets()

    # Removes unwanted emotion tags, forbidden strings and every delimiter but ","
    def cleanup_datasets(self):
        for dataset in self.datasets:
            print("cleaning up dataset", dataset[0])
            # Read the dataset
            self.csv_dataset = pandas.read_csv("corpora/" + dataset[0] + ".csv", delimiter=dataset[1])

            # Choose only the rows annotated with 1 of the 5 emotions
            print("... removing unwanted affect tags")
            self.clean_rows = self.csv_dataset.loc[(self.csv_dataset["affect"] == "happiness") |
                                                   (self.csv_dataset["affect"] == "sadness") |
                                                   (self.csv_dataset["affect"] == "anger") |
                                                   (self.csv_dataset["affect"] == "fear") |
                                                   (self.csv_dataset["affect"] == "disgust")]
            # Reset the index numbers for the rows
            self.clean_rows.reset_index(inplace=True)

            # Delete all rows that contain links or @-mentions
            print("... removing links and mentions")
            self.drop_rows = []
            for index, row in self.clean_rows.iterrows():
                if row["text"].__contains__("http") or row["text"].__contains__("@"):
                    self.drop_rows.append(False)
                else:
                    self.drop_rows.append(True)
            self.drop_rows = pandas.Series(self.drop_rows)
            # Choose only the rows that don't contain links or mentions
            self.clean_rows = self.clean_rows[self.drop_rows]

            # Save these datasets as a cleaned up corpus with delimiter ","
            self.clean_rows.drop(columns=["index"], inplace=True)
            self.clean_rows.to_csv("corpora/" + dataset[0] + "_clean.csv", sep=",")
            print("... done\n")


cleaner = Cleaner()