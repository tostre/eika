import tkinter as tk
import datetime

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

import matplotlib, sys
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
import numpy as np
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

        # create widgets
        self.chatOutWidget = tk.Text(self.root, width=60, state="disabled")
        self.chatInWidget = tk.Entry(self.root)
        self.chatInWidget.bind('<Return>', self.notify_controller)
        self.chatInWidget.focus_set()
        self.logWidget = tk.Text(self.root, width=60, state="disabled")
        self.debugWidget = tk.Text(self.root, width=40, state="disabled")
        self.infoLabel = tk.Label(self.root, text="EIKA v.0.0.1, cMarcel Müller, FH Dortmund ")
        self.button = tk.Button(self.root, text="Send", command=self.notify_controller)
        # create diagram space
        self.diagram_frame = tk.Frame(self.root)
        self.diagram_frame.configure(background="green")
        self.canvas1 = FigureCanvasTkAgg(self.get_figure(), master=self.diagram_frame) # a tk drawingare

        # position ui elements
        self.chatOutWidget.grid(row=1, column=1, columnspan=2)
        self.logWidget.grid(row=1, column=3)
        self.chatInWidget.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.button.grid(row=2, column=2, sticky=tk.E + tk.W)
        #self.debugWidget.grid(row=1, column=4, columnspan=2, sticky=tk.E)
        self.diagram_frame.grid(row=1, column=4, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
        self.infoLabel.grid(row=2, column=4, sticky=tk.E)
        self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # set subscriber list (implements observer pattern)
        self.subscribers = set()

    def get_figure(self):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        # an array of venly spaced numbers
        self.x = np.arange(0, 3, .01)
        self.y = np.sqrt(self.x)
        self.z = np.exp(self.x)

        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(nrows=2, ncols=2)

        self.ax1 = self.get_radar_chart("Bot emotional status", 221)
        self.ax2 = (self.get_radar_chart("conversation dub", 222))
        #self.ax2.plot(self.x, self.x)
        self.ax3.plot(self.z, self.y)
        self.ax4.plot(self.z, self.x)

        self.ax2.set_title("conversation dub")
        self.ax3.set_title("input analysis")
        self.ax4.set_title("output")


        # Benutze diese Methode für polar-Diagramme
        #if method == 1:
            # Both, add_axes and add_subplot add an axes to a figure. They both return a matplotlib.axes.Axes object.

            # add_axes(x0, y0, width, height): Die Parameter geben die Position in der canvas ein
            # Beispiel unten zeichnet ein axes-Objekt von der linken unteren bis in die rechte obere ecke der canvas
            # Das axes-Objekt ist also genauso groß wie die canvas (parameter müssen eine liste sein)
            # Wenn man die Achsen/Labels sehen will, darf das axes nicht bei 0,0 staten. Labels/Achses sind nichT Teil
            # des axes-Objekts und sind daher nicht zu sehen wenn axes bei 0,0 startet
            #### self.ax =self.fig.add_axes([0, 0, 1, 1]).plot(self.x, self.y)

            # add,suplot(xxx): Man bestimmt wo das axes-objekt in einem virtuellen raster erscheint.
            # Bsp: add_suplot(123): Das Raster hat 1 Zeilen und 2 Spalten und man fügt das axes an der 3. Postion ein
            # Bsp: add_sbplot(111): Eine Zeile, eine Spalte. Axes nimmt also die ganze Flächer der canvas ein
            # Der Vorteil dieser Methode: plt macht die Positionierung und lässt genug Platz für die Labels der Achsen etc
            # Die sind nämlich nicht Teil des axes-Objektes und sind bei der Lösung oben daher nicht zu sehen
            #self.ax1 = self.fig.add_subplot(221)
            #self.ax2 = self.fig.add_subplot(222)
            #self.ax3 = self.fig.add_subplot(223)
            #self.ax4 = self.fig.add_subplot(224)

        # Benutze diese Methode für normale Diagramme
        #elif method == 2:
            # Den ganzen oberen Teil kann man auch einfacher haben:
            # Dabei werden die axes dem fig automatisch hinzugefügt
            #### self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(nrows=2, ncols=2)
            # nrows, ncols muss der Struktur der axes in den klammern ensprechen.
            #self.fig, ((self.ax1, self.ax2, self.ax3), (self.ax4, self.ax4, self.ax4,)) = plt.subplots(nrows=2, ncols=3)


        # In most cases, add_subplot would be the prefered method to create axes for plots on a canvas.
        # Only in cases where exact positioning matters, add_axes might be useful.
        return self.fig

    def get_regular_chart(self, title):
        pass

    def get_radar_chart(self, title, position):
        # Voerbereitung. Bei allen Listen muss der erste Wert am Ende wiederholt werden, damit der Kreis einmal
        # ganz rum geht
        self.labels = ["h", "s", "a", "f", "d"]
        self.values = [0.7, 0.6, 0.3, 0.6, 0.5]
        self.values.append(self.values[0])
        self.length = len(self.labels)
        self.angles = [n / float(self.length) * 2 * pi for n in range(self.length)]
        self.angles += self.angles[:1]

        # Erstelle radar chart
        self.ax = plt.subplot(position, polar=True)
        self.ax.set_title(title)
        # Beschrifte die Achsen (x = der Kreis, y = die "Speichen"), ylim = limits der y-Achse
        plt.xticks(self.angles[:-1], self.labels, color='grey', size=10)
        plt.yticks([0.2, 0.4, 0.6, 0.8], [".2", ".4", ".6", ".8"], color="grey", size=8)
        plt.ylim(0, 1)
        # Plot data und fülle die Fläche dazwischen aus
        self.ax.plot(self.angles, self.values, linewidth=.1)
        self.ax.fill(self.angles, self.values, color='blue', alpha=0.1)

        return self.ax

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
