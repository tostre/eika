import frame
import bot
import character

# dicts for traits and emotions
# TODO: Regeln implementieren:
# val ist bei initiierung immer = trait
# val darf nie höher sein als maxVal
# alle werte gehen von 0 bis 1
h = {"trait": 0.3, "val": 0.3, "maxVal": 0.9, "actVal": 0.3}
s = {"trait": 0.1, "val": 0.1, "maxVal": 0.7, "actVal": 0.2}
a = {"trait": 0.2, "val": 0.2, "maxVal": 0.4, "actVal": 0.5}
f = {"trait": 0.0, "val": 0.0, "maxVal": 0.5, "actVal": 0.7}
d = {"trait": 0.1, "val": 0.1, "maxVal": 0.6, "actVal": 0.3}

character = character.newCharacter(h, s, a, f, d)
botName = "EIKA"
bot = bot.newBot(botName, character)
bot.train()

frame = frame.newFrame(botName, bot)
frame.show()

