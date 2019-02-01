# Idee: Der Charakter wird definiert durch:
# 1. Die emo-listen (traits, max_val, act_val
# 2. Welcher state-Wert durch welche anderen Werte beeinflusst wird
# 3. Die Beziehung zu einem anderen Menschen (das beeinflusst welcher
#    Input-Wert welchen emo-Wert wie beeinflusst
# Bsp: Wenn ich jemanden kenne und ich bekomme eine traurige Nachricht,
# werde ich auch traurig. Wenn ich ihn incht kenne, ist mir das egal
import numpy as np
import math


class Character:
    def __init__(self, emotions, trait_values, max_values, act_values):
        # act_val depicts how strongly an emotion is influenced by other emotions. A high anger_act_val means that
        # this person gets mad real quick and overreacts to incoming emotions
        # if an incoming emotion affects the corresponding character-emotion act_val serves as kind of an empathy-value
        # trait_values are the min-value of an emotion
        self.emotions = emotions
        self.act_values = act_values
        self.trait_values = trait_values
        self.max_values = max_values
        self.emotional_state = self.trait_values.copy()

        self.emotional_history = np.zeros((5, 5))
        self.emotional_history[0] = self.emotional_state.copy()

        # saves the last five emotional states, rows = jeweils ein zeitschritt, spalte=jeweils eine emotion
        self.emotional_history = [
            self.emotional_state.copy(),
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]

        # empathy mod related variables
        # gibt an wie eine emotion (zeile) von den andern emotionen (spalten) verändert wird
        # Beisiel erste Reihen, erste Spalte: Der h-Wert des Bots steiert sich um den 0,2-fachen Wert des eingehenden h-Werts
        # Es gibt keinen Threshhold und keinen max-Wert
        # Beispiel zweite Reihe, erste Spalt: Wenn eine Nachricht reinkommt, wird deren 0,2facher-Happiness-Wert vom eigenen sad-Wert abgezogen
        # aber nur wenn der Betrag des Wertes höher dem Threshhold von 0,1 ist
        self.empathy_functions = [
            # rows show the emotions having an influence on the line-emotion
            [[0.05, 0, 0, 1], [0, 0, 0, 1], [-0.05, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]],  # lines show the emotion being influenced (happiness)
            [[-0.05, 0, 0.1, 1], [0.05, 0, 0, 1], [0, 0, 0, 1], [0.05, 0, 0, 1], [0, 0, 0, 1]],  # sadness
            [[-0.05, 0, 0.1, 1], [0, 0, 0, 1], [0.05, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]],  # anger
            [[0, 0, 0, 1], [0, 0, 0, 1], [0.05, 0, 0, 1], [0.05, 0, 0, 1], [0.05, 0, 0, 1]],  # fear
            [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0.05, 0, 0, 1]]  # digust
        ]

        # decay mod related variables
        # values predicting how much an emotional values lowers per round
        self.decay_modifiers_values = np.array([-0.05, -0.05, -0.05, -0.05, -0.05])

        # state modifier related variables
        # Array zeigt, welche Emotionen (Zeilen) von welchen anderen Emotionene (Spalten) mit einem hohen Wert gedämpft/verstärkt werden
        # rows show the emotions having an influence on the line-emotion
        # 1 = kein Einfluss, zw. 0 und 1 = dämpfender einfluss, >1 = verstärkender einfluss, <0 = sorgt für abbau anderer emotionen
        # Die Werte können eingestellt werden, bzw. sind vom Charakter abhängig (sollten als Parameter in der init übergeben werden)
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

    def update_emotional_state(self, input_emotions):
        # Speichert die insgesamten modifier für die 5 Emotionen, Zeilen = Emotionen, Spalten = mods
        self.modifiers = np.zeros((5, 3))
        # Saves the change for one emotion caused by all input emotions
        self.current_emotion_empathy_modifiers = np.zeros(5)

        # reapeat for every emotion the bot has (happiness, sadness, etc.)
        for index, emotion in enumerate(self.emotions, start=0):
            # Apply decay_modifier
            # Every emotion automatically reduces by 0.05 per round
            self.modifiers[index][1] = self.decay_modifiers_values[index]

            # apply empathy modifier
            # repeat for every emotion again, cause every emotion can have an infuence on all other emotions
            for i, function in enumerate(self.empathy_functions[index], start=0):
                # save all the influences on the currently checked emotion (outer loop) in an array
                self.current_emotion_empathy_modifiers[i] = self.linear_function(input_emotions[i], function)
            # sava the sum of all the single empathy mods in the modifier-array
            self.modifiers[index][0] = sum(self.current_emotion_empathy_modifiers)

            # apply state modifier
            # get the state_modifiers for this emotion (outer loop)
            self.current_state_modifiers = self.state_modifiers_values[index].copy()
            # Schaue durch die Liste der state_modifier für diese emotion (outer loop). Wenn der state der beeinflussenden
            # emotion über dem threshhold ist, lasse den wert in der liste stehen, wenn nicht ersetze den mit 1.
            for i, name in enumerate(self.current_state_modifiers, start=0):
                if self.emotional_state[i] <= self.state_modifiers_threshold:
                    self.current_state_modifiers[i] = 1

            # berechne den duchschnitt der state modifier
            self.state_modifier_mean = np.mean(self.current_state_modifiers[index])
            # Multipiliere alle modifier (input, decay, etc.) mit dem durchschnitt des state modifiers für diese emotion
            # Die emotionen die nicht über dem threshold sind, haben hier keinen einfluss, weil sie auf 1 gesetzt wurden
            # d.h. bei der berechnung des durchschnitts wurden sie quasi schon rausgerechnet
            self.modifiers[index] = self.modifiers[index] * self.state_modifier_mean

        # calculate the new emotional state
        self.emotional_state_old = self.emotional_state.copy()
        # addiere den aktuellen emo_state mit den addierten modifiern pro emotion (je eine zeile)
        self.emotional_state = self.emotional_state_old + np.sum(self.modifiers, 1)

        # apply delta modifier
        self.delta_values = np.zeros(4)
        self.deltas = self.emotional_state - self.emotional_state_old
        # delete the first element because we only need the deltas of the nagitive emotions
        self.deltas = np.delete(self.deltas, 0)
        # calc the mean of the deltas
        self.mean_delta = np.mean(self.deltas)
        # check if the mean is below zero, ie the negative emotions shrunk
        if self.mean_delta < 0:
            # add the value of the delta function to the happiness value
            self.emotional_state[0] += self.linear_function(self.mean_delta, self.delta_function)


        print(self.emotional_state)
        print(self.trait_values)
        print(self.max_values)
        # check if all emotions are in range of trait and max values
        for index, value in enumerate(self.emotional_state, start=0):
            if value < self.trait_values[index]:
                print("too small: " + index.__str__() + ", " + value.__str__() + ", " + self.trait_values[index].__str__())
                self.emotional_state[index] = self.trait_values[index]
            elif value > self.max_values[index]:
                print("too small: " + index.__str__() + ", " + value.__str__() + ", " + self.max_values[index].__str__())
                self.emotional_state[index] = self.max_values[index]

        return np.round(self.emotional_state, 3)

    def update_emotional_history(self, emotional_state):
        # Deletes the last entry in the list and copys the ones from the new emo_state to the front
        self.emotional_history = self.emotional_history[:-1]
        self.emotional_history = [self.emotional_state.copy()] + self.emotional_history
        return self.emotional_history

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
