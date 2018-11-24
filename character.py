class newCharacter:
    def __init__(self, h, s, a, f, d):
        self.h = h
        self.s = s
        self.a = a
        self.f = f
        self.d = d
        print("h: " + self.h.__str__())
        print("s: " + self.s.__str__())
        print("a: " + self.a.__str__())
        print("f: " + self.f.__str__())
        print("d: " + self.d.__str__())

    def updateEmotion(self, emotion, newVal):
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
