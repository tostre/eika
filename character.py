# Idee: Der Charakter wird definiert durch:
# 1. Die emo-listen (traits, max_val, act_val
# 2. Welcher state-Wert durch welche anderen Werte beeinflusst wird
# 3. Die Beziehung zu einem anderen Menschen (das beeinflusst welcher
#    Input-Wert welchen emo-Wert wie beeinflusst
# Bsp: Wenn ich jemanden kenne und ich bekomme eine traurige Nachricht,
# werde ich auch traurig. Wenn ich ihn incht kenne, ist mir das egal
import numpy as np
import timeit




# default characters:
# stable character
# reactive/empathatic character
# jähzornig

class Character:
    def __init__(self, emotions, first_launch):
        self.trait_values = []
        self.max_values = []
        self.emotional_state = []
        self.emotional_history = np.zeros((5, 5))
#        self.empathy_functions = np.array()
#        self.decay_modifiers_values = np.array()
        self.state_modifiers_values = []
        self.state_modifiers_threshold = None
        self.delta_function = []
        self.relationship_status = None
        self.relationship_modifiers = {}

        self.emotions = emotions
        self.character_package = {}
        # in the case of the first launch, load default values, else load previous state
        if first_launch:
            self.set_to_defaults()
        else:
            self.load()

    def get_character_package(self):
        self.character_package = {
            "trait_values": self.trait_values,
            "max_values": self.max_values,
            "empathy_functions": self.empathy_functions,
            "decay_modifiers_values": self.decay_modifiers_values,
            "state_modifiers_values": self.state_modifiers_values,
            "state_modifiers_threshold": self.state_modifiers_threshold,
            "delta_function": self.delta_function,
            "relationship_status": self.relationship_status,
            "relationship_modifiers": self.relationship_modifiers
        }

        return self.character_package


    # saves the current character in a npz file
    def save(self):
        np.savez("character",
                 trait_values=self.trait_values,
                 max_values=self.max_values,
                 emotional_state=self.emotional_state,
                 emotional_history=self.emotional_history,
                 empathy_functions=self.empathy_functions,
                 decay_modifiers_values=self.decay_modifiers_values,
                 state_modifiers_values=self.state_modifiers_values,
                 state_modifiers_threshold=self.state_modifiers_threshold,
                 delta_function=self.delta_function,
                 relationship_status=self.relationship_status,
                 relationship_modifiers=self.relationship_modifiers)

    # loads character variables from a npz file
    def load(self):
        self.character_npz = np.load("character.npz")
        self.trait_values = self.character_npz.get("trait_values")
        self.max_values = self.character_npz.get("max_values")
        self.emotional_state = self.character_npz.get("emotional_state")
        self.emotional_history = self.character_npz.get("emotional_history")
        self.empathy_functions = self.character_npz.get("empathy_functions")
        self.decay_modifiers_values = self.character_npz.get("decay_modifiers_values")
        self.state_modifiers_values = self.character_npz.get("state_modifiers_values")
        self.state_modifiers_threshold = self.character_npz.get("state_modifiers_threshold")
        self.delta_function = self.character_npz.get("delta_function")
        self.relationship_status = self.character_npz.get("relationship_status").item()
        self.relationship_modifiers = self.character_npz.get("relationship_modifiers").item()

    def set_to_defaults(self):
        self.trait_values = [0.100, 0.100, 0.100, 0.100, 0.100]
        self.max_values = [0.900, 0.900, 0.900, 0.900, 0.900]
        self.emotional_state = self.trait_values.copy()

        # saves the last five emotional states, rows = jeweils ein zeitschritt, spalte=jeweils eine emotion
        self.emotional_history = np.zeros((5, 5))
        self.emotional_history[0] = self.emotional_state.copy()

        # empathy mod related variables
        # gibt an wie eine emotion (zeile) von den andern emotionen (spalten) verändert wird
        # Beisiel erste Reihen, erste Spalte: Der h-Wert des Bots steiert sich um den 0,2-fachen Wert des eingehenden h-Werts
        # Es gibt keinen Threshhold und keinen max-Wert
        # Beispiel zweite Reihe, erste Spalt: Wenn eine Nachricht reinkommt, wird deren 0,2facher-Happiness-Wert vom eigenen sad-Wert abgezogen
        # aber nur wenn der Betrag des Wertes höher dem Threshhold von 0,1 ist
        self.empathy_functions = np.array([
            [[0.05, 0, 0, 1], [0, 0, 0, 1], [-0.05, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]],  # lines show the emotion being influenced (happiness)
            [[-0.05, 0, 0.1, 1], [0.05, 0, 0, 1], [0, 0, 0, 1], [0.05, 0, 0, 1], [0, 0, 0, 1]],  # sadness
            [[-0.05, 0, 0.1, 1], [0, 0, 0, 1], [0.05, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]],  # anger
            [[0, 0, 0, 1], [0, 0, 0, 1], [0.05, 0, 0, 1], [0.05, 0, 0, 1], [0.05, 0, 0, 1]],  # fear
            [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0.05, 0, 0, 1]]  # digust
        ])

        # decay mod related variables
        # values predicting how much an emotional values lowers per round
        self.decay_modifiers_values = np.array([-0.01, -0.01, -0.01, -0.01, -0.01])

        # state modifier related variables
        # Array zeigt, welche Emotionen (Zeilen) von welchen anderen Emotionene (Spalten) mit einem hohen Wert gedämpft/verstärkt werden
        # 1 = kein Einfluss, zw. 0 und 1 = dämpfender einfluss, >1 = verstärkender einfluss, <0 = sorgt für abbau anderer emotionen
        self.state_modifiers_values = [
            [1, 1, 0.9, -1, 1],  # lines show the emotion being influenced (happiness)
            [0.9, 1.1, 1.1, -1, 1],  # sadness
            [0.9, 1.1, 1.1, -1, 1],  # anger
            [0.9, 1.1, 1.1, -1, 1],  # fear
            [0.9, 1.1, 1.1, -1, 1]  # disgust
        ]
        # Array speichert Wert, der sagt, ab welchem Wert ein state_Wert als "hoch" gilt
        self.state_modifiers_threshold = 0.75

        # delta mod realated variables
        # function that determinces how much happiness raises in relation to the lowering of the neg. emotions
        self.delta_function = [-0.2, 0, 0, 1]

        # relationship modifier
        # saves the kind of relationship the bot has with the user (love/family, friend, neutral, dislike)
        self.relationship_status = "friendship"
        # values impacting the input_emotions (better relationsnship makes you more empathic
        self.relationship_modifiers = {
            "love": 1.3,
            "friendship": 1.2,
            "neutral": 1,
            "dislike": 0.3
        }

    def update_emotional_state(self, input_emotions):
        print(type(input_emotions[0]))
        self.input_emotions = np.array(input_emotions)
        self.debug("input_emotions", self.input_emotions)
        # Speichert die insgesamten modifier für die 5 Emotionen, Zeilen = Emotionen, Spalten = mods
        self.modifiers = np.zeros((5, 3))
        # Saves the change for one emotion caused by all input emotions
        self.current_emotion_empathy_modifiers = np.zeros(5)

        # apply relationship modifier
        # the better the relationship the more empathic you are and take the input seriously
        # check if the inserted relationship status is in the list of relationship modifiers
        if self.relationship_status in self.relationship_modifiers:
            # multiply the inputs with the relationship modifier
            self.input_emotions *= self.relationship_modifiers[self.relationship_status]
            #self.debug("relationship_modifier", self.relationship_modifiers[self.relationship_status])
            #self.debug("input_emotions", self.input_emotions)

        # reapeat for every emotion the bot has (happiness, sadness, etc.)
        for index, emotion in enumerate(self.emotions, start=0):
            # Apply decay_modifier
            # Every emotion automatically reduces by 0.05 per round
            self.modifiers[index][0] = self.decay_modifiers_values[index]

            # apply empathy modifier
            # repeat for every emotion again, cause every emotion can have an infuence on all other emotions
            for i, function in enumerate(self.empathy_functions[index], start=0):
                # save all the influences on the currently checked emotion (outer loop) in an array
                self.current_emotion_empathy_modifiers[i] = self.linear_function(self.input_emotions[i], function)
            # sava the sum of all the single empathy mods in the modifier-array
            self.modifiers[index][1] = sum(self.current_emotion_empathy_modifiers)

            # apply state modifier
            # get the state_modifiers for this emotion (outer loop)
            self.current_state_modifiers = self.state_modifiers_values[index].copy()
            # Schaue durch die Liste der state_modifier für diese emotion (outer loop). Wenn der state der beeinflussenden
            # emotion über dem threshhold ist, lasse den wert in der liste stehen, wenn nicht ersetze den mit 1.
            for i, name in enumerate(self.current_state_modifiers, start=0):
                if self.emotional_state[i] <= self.state_modifiers_threshold:
                    self.current_state_modifiers[i] = 1
            # berechne den duchschnitt der state modifier
            self.state_modifier_mean = np.mean(self.current_state_modifiers)
            # Multipiliere alle modifier (input, decay, etc.) mit dem durchschnitt des state modifiers für diese emotion
            # Die emotionen die nicht über dem threshold sind, haben hier keinen einfluss, weil sie auf 1 gesetzt wurden
            # d.h. bei der berechnung des durchschnitts wurden sie quasi schon rausgerechnet
            self.modifiers[index] = self.modifiers[index] * self.state_modifier_mean

        # calculate the new emotional state
        self.emotional_state_old = self.emotional_state.copy()
        # addiere den aktuellen emo_state mit den addierten modifiern pro emotion (je eine zeile)
        self.emotional_state = self.emotional_state_old + np.sum(self.modifiers, 1)
        self.debug("modifiers", self.modifiers)
        self.debug("modifiers sum", np.sum(self.modifiers, 1))
        #self.debug("emo state old", self.emotional_state_old)
        #self.debug("modifiers", self.modifiers)
        #self.debug("emo state", self.emotional_state)

        # apply delta modifier
        # delete the first element because we only need the deltas of the nagitive emotions
        self.deltas = np.delete(self.emotional_state - self.emotional_state_old, 0)
        # calc the mean of the deltas
        self.mean_delta = np.mean(self.deltas)
        # check if the mean is below zero, ie the negative emotions shrunk
        # TODO bei der Delta-Funktion kommen glaube ich immer positive Zahlen raus, ist das richtig so?
        if self.mean_delta < 0:
            # add the value of the delta function to the happiness value
            self.debug("delta", self.linear_function(self.mean_delta, self.delta_function))
            self.emotional_state[0] += self.linear_function(self.mean_delta, self.delta_function)

        # check if all emotions are in range of trait and max values
        for index, value in enumerate(self.emotional_state, start=0):
            if value < self.trait_values[index]:
                self.emotional_state[index] = self.trait_values[index]
            elif value > self.max_values[index]:
                self.emotional_state[index] = self.max_values[index]

        # Round emotional state values so they can be used for further calculations
        self.emotional_state = np.round(self.emotional_state, 3)
        # update emotional history
        # inserts emotional state at position 0 on axis 0 into emotional_history
        self.emotional_history = np.insert(self.emotional_history, 0, self.emotional_state, 0)
        self.emotional_history = np.delete(self.emotional_history, 5, 0)

        return self.emotional_state, self.emotional_history

    # Returns the calculation of a linear function
    def linear_function(self, x, function):
        # a function is an array and built as such:
        # f[0] = m (steigung), f[1] = b (Achsenabschnitt), f[2] = t (threshhold), f[3] = m (max-wert den die funktion annhemen kann)
        self.function_result = (function[0] * x) + function[1]

        # check if function result is within min (threshold) and max value
        if abs(self.function_result) <= function[2]:
            return 0
        elif abs(self.function_result) >= function[3]:
            return function[3]
        else:
            return self.function_result

    def linear_function_two(self, x, function):
        pass

    def debug(self, name, var):
        print(name, ": \n", var)

    def get_emotional_state(self):
        return self.emotional_state

    def get_emotional_history(self):
        return self.emotional_history

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
