import tkinter as tk
import datetime

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

import matplotlib, sys
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Frame:
    def __init__(self, cbName, bot, emotion_titles, emotional_state):
        # initialise variables
        self.cbName = cbName
        self.bot = bot
        self.emotion_titles = emotion_titles
        self.emotional_state = emotional_state
        self.input = None
        self.response = None
        self.logOut = None
        self.successMessage = None
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

        # create root-window
        self.root.configure(menu=self.menubar)
        self.root.title(cbName)
        self.root.resizable(0, 0)

        # create chatOut
        self.chatOutWidget = tk.Text(self.root, width=60, state="disabled")
        # create chatIn
        self.chatInWidget = tk.Entry(self.root)
        self.chatInWidget.bind('<Return>', self.notify_controller)
        self.chatInWidget.focus_set()
        # createLog
        self.logWidget = tk.Text(self.root, width=60, state="disabled")
        # createDebug
        self.debugWidget = tk.Text(self.root, width=40, state="disabled")

        # create diagram space
        self.diagram_frame = tk.Frame(self.root)
        self.diagram_frame.configure(background="green")
        self.canvas = tk.Canvas(self.diagram_frame, background="yellow")

        # cerate misc widgets
        self.infoLabel = tk.Label(self.root, text="EIKA v.0.0.1, cMarcel Müller, FH Dortmund ")
        self.button = tk.Button(self.root, text="Send", command=self.notify_controller)


        #self.canvas = tk.Canvas(self.diagram_frame, width = 60, height = 60)
        #self.diagram_frame.configure(width=60, background="green")


        # position ui elements
        self.chatOutWidget.grid(row=1, column=1, columnspan=2)
        self.logWidget.grid(row=1, column=3)
        self.chatInWidget.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.button.grid(row=2, column=2, sticky=tk.E + tk.W)
        #self.debugWidget.grid(row=1, column=4, columnspan=2, sticky=tk.E)
        self.diagram_frame.grid(row=1, column=4, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
        #self.diagram_frame.grid_columnconfigure(0, weight=1)
        #self.canvas.grid(row=1, column=1)
        self.canvas.pack(expand=1)
        #self.canvas.grid_columnconfigure()
        #self.canvas.grid(row=1, column=3)
        #self.diagram_frame.grid(row=1, column=3)
        #self.canvas.create_rectangle(10, 50, 15, 50, fill="blue")
        #self.canvas.configure(background = "yellow")
        self.infoLabel.grid(row=2, column=4, sticky=tk.E)

        # set subscriber list (implements observer pattern)
        self.subscribers = set()

    def draw(self):
        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        a.plot(t, s)

        self.canvas = FigureCanvasTkAgg(f, master=self.root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #dataPlot = FigureCanvasTkAgg(f, master=master)
        #dataPlot.show()
        #dataPlot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def draw_radar_chart(self, emotional_state):
        # We are going to plot the first line of the data frame.
        # But we need to repeat the first value to close the circular graph:
        # appends the list with the first item in the list
        emotional_state.append(emotional_state[0])
        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(5) * 2 * pi for n in range(5)]
        angles += angles[:1]
        # Initialise the spider plot
        ax = plt.subplot(111, polar=True)
        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], self.emotion_titles, color='grey', size=8)
        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=7)
        plt.ylim(0, 1)
        # Plot data
        ax.plot(angles, emotional_state, linewidth=1, linestyle='solid')
        # Fill area
        ax.fill(angles, emotional_state, 'b', alpha=0.1)
        plt.show()

    # the following two function implement the observer pattern
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
       # self.diagram = Diagrams()
        self.root.mainloop()


class Diagrams:

    def __init__(self):
        master = tk.Tk()

        w = tk.Canvas(master, width=200, height=100)
        w.pack()

        w.create_line(0, 0, 200, 100)
        w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

        w.create_rectangle(50, 25, 150, 75, fill="blue")

        tk.mainloop()
