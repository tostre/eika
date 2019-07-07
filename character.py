import numpy as np
import logging


class Character:
    # constructs a character instance
    def __init__(self, emotions, first_launch):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.emotions = emotions
        self.character_package = {}

        # in the case of the first launch, load default values, else load previous state
        if first_launch:
            self.load("character_default")
        else:
            self.load("character_saved")

    # loads character variables from a npz file
    def load(self, file):
        self.character_npz = np.load("characters/" + file + ".npz")
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
        self.logger.info(f"Session start. {file} loaded")

    # saves the current character in a npz file
    def save(self):
        np.savez("characters/character_saved",
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
        self.logger.info("Session end. character_saved saved.")

    # resets character state (emotional state/history)
    def reset_bot(self):
        self.emotional_state = self.trait_values.copy()
        self.emotional_history = np.zeros((5, 5))
        self.emotional_history[0] = self.emotional_state.copy()
        self.logger.info("Character state reset")

    # updates internal emotional state/history based on input emotions
    def update_emotional_state(self, input_emotions):
        self.logger.info(f"------ old emotional state: {self.emotional_state}")
        self.logger.info(f"Input_emotions: {input_emotions}")
        self.input_emotions = np.array(input_emotions)
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
            self.logger.info(f"for relationship {self.relationship_status}, relationship modifier with value {self.relationship_modifiers[self.relationship_status]}")

        # reapeat for every emotion the bot has (happiness, sadness, etc.)
        for index, emotion in enumerate(self.emotions, start=0):
            # Apply decay_modifier
            # Every emotion automatically reduces by 0.05 per round
            self.modifiers[index][0] = self.decay_modifiers_values[index]
            self.logger.info(f"for emotion {emotion}, decay modifier with value {self.decay_modifiers_values[index]}")

            # apply empathy modifier
            # repeat for every emotion again, cause every emotion can have an infuence on all other emotions
            for i, function in enumerate(self.empathy_functions[index], start=0):
                # save all the influences on the currently checked emotion (outer loop) in an array
                self.function = function
                self.a = self.empathy_functions[index]
                self.current_emotion_empathy_modifiers[i] = self.linear_function(self.input_emotions[i], function)
            # sava the sum of all the single empathy mods in the modifier-array
            self.modifiers[index][1] = sum(self.current_emotion_empathy_modifiers)
            #self.logger.info(f"for emotion {emotion}, empath functions {self.empathy_functions}")
            #self.logger.info(f"for emotion {emotion}, empathy modifier with summed value {self.modifiers[index][1]}")

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
            self.logger.info(f"for emotion {emotion}, state modifier with mean value {self.state_modifier_mean}")
            # Multipiliere alle modifier (input, decay, etc.) mit dem durchschnitt des state modifiers für diese emotion
            # Die emotionen die nicht über dem threshold sind, haben hier keinen einfluss, weil sie auf 1 gesetzt wurden
            # d.h. bei der berechnung des durchschnitts wurden sie quasi schon rausgerechnet
            self.modifiers[index] = self.modifiers[index] * self.state_modifier_mean

        # calculate the new emotional state
        self.emotional_state_old = self.emotional_state.copy()
        # addiere den aktuellen emo_state mit den addierten modifiern pro emotion (je eine zeile)
        self.emotional_state = self.emotional_state_old + np.sum(self.modifiers, 1)
        self.logger.info(f"Summed modifiers: {np.sum(self.modifiers, 1)}")

        # check if all emotions are in range of trait and max values
        self.emotional_state = self.clean_state(self.emotional_state)

        # apply delta modifier
        # delete the first element because we only need the deltas of the nagitive emotions
        self.deltas = np.delete(self.emotional_state - self.emotional_state_old, 0)
        print(self.emotional_state)
        print(self.emotional_state_old)
        print(self.deltas)
        print(self.delta_function)
        # calc the mean of the deltas
        self.mean_delta = np.mean(self.deltas)
        print(np.mean(self.deltas))
        # check if the mean is below zero, ie the negative emotions shrunk
        # TODO bei der Delta-Funktion kommen glaube ich immer positive Zahlen raus, ist das richtig so?
        if self.mean_delta < 0:
            # add the value of the delta function to the happiness value
            self.emotional_state[0] += self.linear_function(self.mean_delta, self.delta_function)
            self.logger.info(f"delta modifier: {self.linear_function(self.mean_delta, self.delta_function)}")

        # check if all emotions are in range of trait and max values
        self.emotional_state = self.clean_state(self.emotional_state)

        # update emotional history
        # inserts emotional state at position 0 on axis 0 into emotional_history
        self.emotional_history = np.insert(self.emotional_history, 0, self.emotional_state, 0)
        self.emotional_history = np.delete(self.emotional_history, 5, 0)

        self.logger.info(f"------ new emotional state: {self.emotional_state}")

        return self.emotional_state, self.emotional_history

    # checks max and min value und sets values accordingly and rounds values
    def clean_state(self, emotional_state):
        # check if all emotions are in range of trait and max values
        for index, value in enumerate(emotional_state, start=0):
            if value < self.trait_values[index]:
                emotional_state[index] = self.trait_values[index]
            elif value > self.max_values[index]:
                emotional_state[index] = self.max_values[index]
        # Round emotional state values so they can be used for further calculations
        emotional_state = np.round(self.emotional_state, 3)
        return emotional_state

    # Returns the calculation of a linear function
    def linear_function(self, x, function):
        # a function is an array and built as such:
        # f[0] = m (steigung), f[1] = b (Achsenabschnitt), f[2] = t (threshhold), f[3] = m (max-wert den die funktion annhemen kann)
        self.function_result = (function[0] * x) + function[1]

        # check if function result is within min (threshold) and max value
        if abs(self.function_result) <= function[2] or x == 0:
            return 0
        elif abs(self.function_result) >= function[3]:
            return function[3]
        else:
            return self.function_result

    # Returns the current emotional state
    def get_emotional_state(self):
        return self.emotional_state

    # Returns the emotional history
    def get_emotional_history(self):
        return self.emotional_history