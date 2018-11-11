import tkinter as tk
import datetime

class newFrame:
    def __init__(self, cbName, bot):
        self.cbName = cbName
        # get bot instance from controller
        self.bot = bot
        # widget initialization
        self.root = tk.Tk()
        # create menubar
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Edit bot personality")
        self.filemenu.add_command(label="Edit bot mood")
        self.filemenu.add_command(label="Edit bot emotions")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Retrain chatbot", command=self.retrainBot)
        self.menubar.add_cascade(label="Configure", menu=self.filemenu)
        # create interactive widgets
        self.info = tk.Label(self.root, text="EIKA v.0.0.1, cMarcel Müller, FH Dortmund ")
        self.chatOut = tk.Text(self.root)
        self.chatIn = tk.Entry(self.root)
        self.debug = tk.Text(self.root)
        self.log = tk.Text(self.root)
        # modify ui
        self.root.title(cbName)
        self.root.resizable(0,0)
        self.button = tk.Button(self.root, text="Send", command=self.updateChatOut)
        self.chatIn.bind('<Return>', self.hitEnter)
        self.chatIn.focus_set()
        self.chatOut.configure(state="disabled")
        self.log.configure(state="disabled")
        self.log.configure(width=40)
        self.debug.config(width=40)
        self.debug.configure(state="disabled")
        # build layout
        self.root.configure(menu=self.menubar)
        self.chatOut.grid(row=1, column=1, columnspan=2)
        self.log.grid(row=1, column=3)
        self.chatIn.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.button.grid(row=2, column=2, sticky=tk.E + tk.W)
        self.debug.grid(row=1, column=4, columnspan=2, sticky=tk.E)
        self.info.grid(row=2, column=4, sticky=tk.E)

    def retrainBot(self):
        self.result = self.bot.train()
        self.updateDebug(self.result)


    # bidns the enter key to updateChatOut
    def hitEnter(self, event):
        self.updateChatOut()

    # called when button is clicked/enter pressed, handles in/output
    def updateChatOut(self):
        self.input = self.chatIn.get()
        # prüft ob in dem string was drinsteht
        if input:
            # prints input, empties input field
            self.chatOut.configure(state="normal")
            self.chatOut.insert(tk.END, "Du: " + self.input + "\n")
            self.chatOut.see(tk.END)
            # deletes text from index 0 till the end in input filed
            self.chatIn.delete(0, tk.END)
            # inserts chatbot answer in chat
            self.chatOut.insert(tk.END, self.cbName + ": " + self.bot.respond(self.input) + "\n")
            self.chatOut.configure(state="disabled")

    # prints to the debug widget
    def updateDebug(self, debug):
        # get time
        t = datetime.datetime.now()
        time = str(t.hour) + ":" + str(t.minute) + ":" + str(t.second)
        # unlock widget, inster, lock widget
        self.debug.configure(state="normal")
        self.debug.insert(tk.END, time + ": " + debug + "\n")
        self.debug.configure(state="disabled")

    # prints to the log widget
    # used to display additional text data (sentiment etc)
    def updateLog(self, log):
        pass

    def show(self):
        self.root.mainloop()