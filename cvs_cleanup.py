import csv
import pandas

class Cleaner:
    def __init__(self):
        self.datasets = [["crowdflower", ","], ["emoint", "\t"],
                         ["emotion_classification", ","],
                         ["isear", "\t"], ["meld", ","], ["tec", "\t"]]
        #self.datasets = [["crowdflower", ","]]
        self.emotions = ["happiness", "sadness", "anger", "fear", "disgust"]
        self.test_emotions = ["neutral", "happiness"]
        self.test_line = ["greeting you all a happy mother's day!", 'happiness']




        #self.lists_have_common_member(self.emotions, self.test_line)

        #self.clean_delimiter()
        self.pandas_teset()
        pass

    def pandas_teset(self):
        for dataset in self.datasets:
            print("cleaning up dataset", dataset[0])
            # Read the dataset
            self.dataset = pandas.read_csv("corpora/" + dataset[0] + ".csv", delimiter=dataset[1])
            # Choose only the rows annotated with 1 of the 5 emotions
            self.emotion_rows = self.dataset.loc[(self.dataset["affect"] == "happiness") |
                                      (self.dataset["affect"] == "sadness") |
                                      (self.dataset["affect"] == "anger") |
                                      (self.dataset["affect"] == "fear") |
                                      (self.dataset["affect"] == "disgust")]
            # Save these datasets as a cleaned up corpus
            self.emotion_rows.to_csv("corpora/" + dataset[0] + "_clean.csv", sep=",")
            print("... finished")



    # replaces any other delimiter with a comma
    def clean_delimiter(self):
        for dataset in self.datasets:
            with open("corpora/" + dataset[0] + ".csv", "r") as file:
                reader = csv.reader(file, delimiter=dataset[1])
                with open("corpora/" + dataset[0] + "_clean.csv", "w") as new_file:
                    writer = csv.writer(new_file, delimiter=",")

                    for line in reader:
                        print(line)

                        # check if the lines are only tagged with the 5 main emotions
                        # check if the does not contain a link
                        # check if the does not contain a @-mention
                        if self.lists_have_common_member(self.emotions, line)\
                                and not any("http" in string for string in line)\
                                and not any("@" in string for string in line):
                            # save clean file with ","-delimiter if all conditions are met
                            writer.writerow(line)
                        else:
                            # ignore the line if not all conditions are met
                            print("Line ommited: ", line)
                            pass




    def lists_have_common_member(self, list1, list2):

        for list1_item in list1:
            for list2_item in list2:
                if list1_item == list2_item:
                    #print("Emotion gefunden: ", list1_item + ", ", list2_item)
                    return True

        #print("Emotionen nicht gefunden")
        return False



cleaner = Cleaner()