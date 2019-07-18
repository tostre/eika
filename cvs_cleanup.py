import csv

class Cleaner:
    def __init__(self):
        #self.datasets = ["crowdflower", "emoint", "emotion_classification", "isear", "meld", "tec"]
        self.datasets = ["crowdflower"]
        self.emotions = ["happiness", "sadness", "anger", "fear", "disgust"]
        self.test_emotions = ["neutral", "happiness"]
        self.test_line = ["greeting you all a happy mother's day!", 'happiness']

        #self.lists_have_common_member(self.emotions, self.test_line)

        self.clean_delimiter()

        pass

    # replaces any other delimiter with a comma
    def clean_delimiter(self):
        for dataset in self.datasets:
            with open("korpora/" + dataset + ".csv", "r") as file:
                reader = csv.reader(file)
                with open("korpora/" + dataset + "_clean.csv", "w") as new_file:
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