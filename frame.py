import tkinter as tk
import datetime


class Frame:
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
        self.filemenu.add_command(label="Retrain chatbot", command=self.retrain_bot)
        self.menubar.add_cascade(label="Configure", menu=self.filemenu)
        # create interactive widgets
        self.infoLabel = tk.Label(self.root, text="EIKA v.0.0.1, cMarcel Müller, FH Dortmund ")
        self.chatOutWidget = tk.Text(self.root)
        self.chatInWidget = tk.Entry(self.root)
        self.debugWidget = tk.Text(self.root)
        self.logWidget = tk.Text(self.root)
        # modify ui
        self.root.title(cbName)
        self.root.resizable(0, 0)
        self.button = tk.Button(self.root, text="Send", command=self.notify_controller)
        self.chatInWidget.bind('<Return>', self.notify_controller)
        self.chatInWidget.focus_set()
        self.chatOutWidget.config(width=60)
        self.chatOutWidget.configure(state="disabled")
        self.logWidget.configure(state="disabled")
        self.logWidget.configure(width=60)
        self.debugWidget.config(width=40)
        self.debugWidget.configure(state="disabled")
        # build layout
        self.root.configure(menu=self.menubar)
        self.chatOutWidget.grid(row=1, column=1, columnspan=2)
        self.logWidget.grid(row=1, column=3)
        self.chatInWidget.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.button.grid(row=2, column=2, sticky=tk.E + tk.W)
        self.debugWidget.grid(row=1, column=4, columnspan=2, sticky=tk.E)
        self.infoLabel.grid(row=2, column=4, sticky=tk.E)
        #
        self.input = None
        self.response = None
        self.logOut = None
        self.successMessage = None
        #
        self.subscribers = set()

    def register(self, controller):
        # self.subscribers.add(who)
        self.controller = controller

    def notify_controller(self, event):
        self.input = self.chatInWidget.get()
        if self.input:
            self.controller.handle_input(self.input)

    def retrain_bot(self):
        self.successMessage = self.bot.train()
        self.updateDebug(self.successMessage)

    # prints in chatout widget
    def updateChatOut(self, input, response):
        # prints input, empties input field
        self.chatOutWidget.configure(state="normal")
        self.chatOutWidget.insert(tk.END, "Du: " + input + "\n")
        # deletes text from index 0 till the end in input filed
        self.chatInWidget.delete(0, tk.END)
        # inserts chatbot answer in chat
        self.chatOutWidget.insert(tk.END, self.cbName + ": " + response + "\n")
        self.chatOutWidget.see(tk.END)
        self.chatOutWidget.configure(state="disabled")

    # prints to the log widget, used to display additional text data (sentiment etc)
    def updateLog(self, output):
        # unlock widget, inster, lock widget
        self.logWidget.configure(state="normal")
        self.logWidget.delete(1.0, tk.END)
        # print out emototional relevant word counts (normalized)
        for item in output:
            self.logWidget.insert(tk.END, item + "\n")
        self.logWidget.configure(state="disabled")

    # prints to the debug widget
    def updateDebug(self, debug):
        # get time
        t = datetime.datetime.now()
        time = str(t.hour) + ":" + str(t.minute) + ":" + str(t.second)
        # unlock widget, inster, lock widget
        self.debugWidget.configure(state="normal")
        self.debugWidget.insert(tk.END, time + ": " + debug + "\n")
        self.debugWidget.configure(state="disabled")

    def show(self):
        self.root.mainloop()
