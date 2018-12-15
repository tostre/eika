import math
import numpy as np
import matplotlib.pyplot as plt

# Idee: Der Charakter wird definiert durch:
# 1. Die emo-listen (traits, max_val, act_val
# 2. Welcher state-Wert durch welche anderen Werte beeinflusst wird
# 3. Die Beziehung zu einem anderen Menschen (das beeinflusst welcher
#    Input-Wert welchen emo-Wert wie beeinflusst
# Bsp: Wenn ich jemanden kenne und ich bekomme eine traurige Nachricht,
# werde ich auch traurig. Wenn ich ihn incht kenne, ist mir das egal
class Character:
    def __init__(self, trait_values, max_values, act_values):
        self.trait_values = trait_values
        self.max_values = max_values
        self.act_values = act_values

        # set emotional state to trait (aka min-) values
        self.emotional_state = [
            self.trait_values[0],
            self.trait_values[1],
            self.trait_values[2],
            self.trait_values[3],
            self.trait_values[4]]
        # 1 = positive relation, 0, negative relation
        # 0 happiness
        # 1 sadness
        # 2 anger
        # 3 fear
        # 4 disgust
        self.input_modificators = {
            0: [[0, 1], [2, 0]],
            1: [[0, 0], [1, 1], [3, 1]],
            2: [[0, 0], [2, 1]],
            3: [[2, 1], [3, 1], [4, 1]],
            4: []
        }

        self.input_modificators = {
            0: [[1, 0, 1, 0, 0], [1, 0, -1, 0, 0]],
            1: [[1, 1, 0, 1, 0], [-1, 1, 0, 1, 0]],
            2: [[1, 0, 1, 0, 0], [-1, 0, 1, 0, 0]],
            3: [[0, 0, 1, 1, 1], [0, 0, 1, 1, 1]],
            4: [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        }

        self.state_modificators = {}

    def up(self, input_emotions):
        self.input_emotions = input_emotions
        self.input_emotions = [0.32, 0.12, 0.07, 0.73, 0.20]
        # hier am beispiel von happiness

        # 0 = happiness
        self.emotion = 0
        #print("emotion: " + self.emotion.__str__())
        self.old_val = self.emotional_state[self.emotion]
        #print("old_val: " + self.old_val.__str__())


        self.updaters = [[],[],[],[],[]]

        print(len(self.input_modificators))
        #for item in range(len(self.input_modificators)):
        for index in range(len(self.input_modificators)):
            print("\n__________________________________________________________________________________________________________________________________________________________")
            print("\nemotion: " + index.__str__() + ", mods: " + self.input_modificators[index].__str__())
            self.single_emotion_modificaors = self.input_modificators[index]
            self.which_ones = self.input_modificators[index][0]
            self.how = self.input_modificators[index][1]
            self.act = self.act_values[index]

            for index2 in range(len(self.which_ones)):
                print("\nemotion: " + index2.__str__() + ", has Inflicene?: " + self.which_ones[index2].__str__()  + ", input: " + input_emotions[index2].__str__() + ", how: " + self.how[index2].__str__() + ", act: " + self.act.__str__() + ", old_val: " + self.emotional_state[index].__str__())
                self. updater = input_emotions[index2] * self.which_ones[index2] * self.how[index2] * self.act
                print("updater: " + self.updater.__str__())
                self.updaters[index].append(self.updater)
                self.emotional_state[index] = round((self.emotional_state[index]  + self.updater), 2)
                print("new val: " + self.emotional_state[index].__str__())

            print("updater array for emotion " + index.__str__() + " : " + self.updaters.__str__())

        print("updater: " + self.updaters.__str__())

    # Wichtige erkenntnisse: Negative emotionen überschatten positive (quellen)
    # wenn man sauer oder traurig ist, denkt man nur noch an das negative
    # deshalben sollten negative emotionen die positiven nach unten drücken
    # (d.h. mehr effekt haben als die positiven, bzw. diese unterdrücken)
    # außerdem sollten emotionen mit jedem zeitschritt (zB jede nachricht) abnehmen
    def update_emotional_state(self, input_emotions):
        pass
        # ich nehme surprise raus. Ist nur eine kurze reaktion auf ein event
        # das müsste man ganz anders behandeln als den rest der emotionen
        # es eignet sich außerdem nicht als personality trait
        # emotioen treten nur als einzelne werte auf, nicht in einem vektor
        # es können trotzdem mehrere emotionen zugleich auftreten
        # das gleiche gilt für stimmungen
        # Idee: Jede Emotion als Tupel beschreiben
        # Die "Höhe der Emotion von 0 bis 1"
        # Der Aktivierungswert: Beschreibt wie schnell sich diese Emotion aufbauen kann

    def update_happiness(self, input_emotions):
        # base calc happiness und anger
        self.new_hap = self.emotional_state[0] + (input_emotions[0] * self.act_values[0])
        print("new hap: " + self.new_hap.__str__())


    def get_emotional_state(self):
        return self.emotional_state

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def function(self, type, x):
        x = np.linspace(0, 100, 100)
        y = np.sin(4*x)
        y = 1 / (1 + np.exp(-x))
        # creates a figure with index 1
        plt.figure(1)
        plt.plot(x, y)
        #plt.plot([1, 2, 3, 4], [7, 1, 7, 5])
        # The axis() command in the example above takes a list of [xmin, xmax, ymin, ymax] and specifies the viewport of the axe
        #plt.axis([0, 6, 0, 20])
        #plt.ylabel('some numbers')
        plt.show()

        if type == "sigmoid":
            return 1 / (1 + np.exp(-x))



# sentiment analysis
# liu et al 2003
# (SVOO-Modell) wandelt einen OMCS-Satz in Frame und zugehörigen Vektor um. Frame enthält alle für die Aussagen des Satzes relevanten Wörter
# und der Vektor beschreibt den in diesem Satz ausgedrückten Affekt (Bsp.: (happy: 0, sad: 0, anger: 0, fear: 1.0, disgust: 0, surprise: 0)

# stimmungen
# emotionen

# Kategoriale Ansätze:
# Differentielle Emotiontheorie:
# 1. von Interesse zu Erregung
# 2. von Vergnügen zu Freude
# 3. von Überraschung zu Schreck
# 4. von Kummer zu Schmerz
# 5. von Zorn zu Wut
# 6. von Ekel zu Abscheu
# 7. von Geringschätzung zu Verachtung
# 8. von Furcht zu Entsetzen
# 9. von Scham/Schüchernheit zu Erniedrigung
# 10. von Schuldgefühle zu Reue
#
# Man unterscheidet zwischen dem Zustand und der Eigenschaft einer EmotionIzard (1999), f..
# Emotionszustände dauern Sekunden bis Stunden und meinen das tatsächliche, jetzige Erleben dieser Emotion.
# Eine Emotionseigenschaft ist die Veranlagung eines Individuums ein bestimmtes Gefühl regelmäßig und wiederholt
# zu erleben (denke: Jähzorn).
#
# Ekman bestimmte Freude, Traurigkeit, Überraschung, Ekel, Furcht und Wut als Grundemotionen
# (Angst und Überrasschung und Ekel und Verachtung werden beizeiten zusammengefasst).
#
# Traurigkeit, Freude, Angst und Ärger in allen fünf Studien benannt wurdenSchmidt-Atzert
# (1996)Brandstätter et al. (2013, S. 132 f.). Ekel, Scham, Zuneigung und Überraschung kamen nur vereinizelt vor.
#
# Dimensionaler Ansatz:
# drei bipolare Dimensionen auf: Lust-Unlust, Erregung-Beruhigung und Spannung-Lösung. Die Lust-Unlust-Skala
# beschreibt die Qualität der Emotion, ob sie also als eher positiv oder eher negativ erlebt wird. Auf die
# Erregung-Beruhigung-Skala wird die erlebte Intensität der Emotion aufgetragen. Diese beiden Dimensionen
# einer Emotion ließen sich empirisch wiederholt bestätigen, die Spannug-Lösung-Dimension nur in einzelnen Fällen.
#
#
# persönlichkeit
# OCEAN-Modell, ordnet Menschen verschiedenen Persönlichkeitstypen zu: Offenheit (gegenüber neuen Erfahrungen),
# Gewissenhaftigkeit, Extraversion, Verträglichkeit und Neurotizismus
#
# ich baue meine persönlichkeit am besten nach wilson (2000) mit ein bissl eismann
# Wenn es eine vorübergehende Emotion gibt, wird das Verhalten, beziehungsweise die Motivation, daraus berechnet.
# Gibt es zur Zeit keine Reaktion wird dazu die Stimmung genutzt. Liegen vorübergehende Emotion und Stimmung unter
# einem bestimmten Schwellenwert, bestimmt die Persönlichkeit das Verhalten.
# Das personality-Modul enthält die mathematische Beschreibung der Persönlichkeit des Carakters. Sie wird über eine
# Kugel in einem dreidimensionalen mathematischen Raum bestimmtWilson (2000, S. 82). Die Achsen beschreiben je ein
# Persönlichkeitsmerkmal, extroversion, fear und aggression. Ein Persönlichkeitsmerkmal ist ein Punkt in diesem Raum.
# Das Merkmal anxiety beispielsweise liegt bei (E: -30, F: 70, A: -10). Um alle Persönlichkeitsmerkmale eines
# Charkaters wird eine Kugel gespannt, die dann die gesamte Persönlichkeit ausmacht.
# Stimmungen werden im mood-Module berechnet gespeichert. Sie werden durch die Persönlichkeit beeinflusstWilson (2000, S. 83).
# Hat der Persönlichkeitspunkt, der Mittelpunkt der Kugel um alle Persönlichkeitsmerkmale, einen hohen E-Wert, können auch
# positive Stimmungen einen höheren Wert annehmen. ein hoher F–Wert ermöglicht hohe Werte von negativen Emotionen und der A-Wert
# bestimmt wie schnell sich diese Stimmungen aufbauen und wieder verfliegen können. Ein Charakter, der sehr hohe Wert in allen
# drei Dimensionen hat, kann starke positive und negative Stimmungen haben, die sich aber sehr schnell ändern können, wie bei
# einem Menschen mit starken Stimmungsschwankungen.
# Stimmungen entwickeln sich hier durch kumulierte emotionale Zustände
#
# EISMAN et al
# Eisman et al. haben es sich im Rahmen eines Forschungsprojektes, das die Entwicklung eines virtuellen Patienten zur Ausbildung
# von Medizinstudenten zum Ziel hatte, zur Aufgabe gemacht, ein emotional state control system zu entwickelnEisman et al. (2009, S. 9698).
# Dieses System basiert auf zwei Faktoren: Dem emotionalen Zustand eines Konversationsagenten und seiner Persönlichkeit. Ein emotionaler
# Zustand besteht aus der spezifischen Zusammensetzung aller Werte (jeweils zwischen 0 und 1) der acht emotionalen Attribute
# (Freude, Verachtung, Wut, Angst, Sorge, Überrasschung, Trauer, Scham)Eisman et al. (2009, S. 9701). Die Persönlichkeit wird über die
# gleichen Attribute bestimmt, die in diesem Fall aber statisch sind.

# stichwörter die hier noch reinmüssen: congruency (trait/mood)
