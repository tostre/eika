import tkinter as tk
import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas


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
        self.dgm = DiagramManager()

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
        self.fig = Figure()
        self.diagram_canvas = FigureCanvas(self.dgm.get_figure(), master=self.diagram_frame) # a tk drawingare

        # position ui elements
        self.chatOutWidget.grid(row=1, column=1, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
        self.logWidget.grid(row=1, column=3, sticky=tk.E+tk.W+tk.N+tk.S)
        self.chatInWidget.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.button.grid(row=2, column=2, sticky=tk.E + tk.W)
        #self.debugWidget.grid(row=1, column=4, columnspan=2, sticky=tk.E)
        self.diagram_frame.grid(row=1, column=4, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)
        self.infoLabel.grid(row=2, column=4, sticky=tk.E)
        self.diagram_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # set subscriber list (implements observer pattern)
        self.subscribers = set()

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
        self.root.mainloop()


class DiagramManager:

    def __init__(self):
        self.list_length = 5
        # Bei allen Listen muss der erste Wert am Ende wiederholt werden, damit der Kreis einmal rum geht
        self.polar_angles = [n / float(self.list_length) * 2 * np.pi for n in range(self.list_length)]
        self.polar_angles += self.polar_angles[:1]
        # position and names for the markers on the x- and y-axis
        self.xticks_labels = ["h", "s", "a", "f", "d"]
        self.yticks_positions = [0.2, 0.4, 0.6, 0.8]
        self.yticks_labels = [".2", ".4", ".6", ".8"]
        self.polar_data = None

    def get_figure(self):
        # create data to display in regular diagrams
        self.past_data = [[-4, -3, -2, -1, 0], [0.7, 0.8, 0.75, 0.6, 0.7]]
        self.past_data2 = [[-4, -3, -2, -1, 0], [0.1, 0.2, 0.1, 0.4, 0.3]]
        self.bar_data = [0.1, 0.2, 0.1, 0.4, 0.3]
        # Vorbereitung. Bei allen radar-Listen muss der erste Wert am Ende wiederholt werden, damit der Kreis einmal rum geht
        self.polar_data = [0.1, 0.6, 0.3, 0.6, 0.5]
        self.polar_data.append(self.polar_data[0])
        self.x = np.arange(0, 3, .01)
        self.y = np.sqrt(self.x)
        self.z = np.exp(self.x)

        # create figures and axes (kind of a subfigure)
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(nrows=2, ncols=2)
        self.make_radar_chart(self.ax1, "Input emotions", 221, self.polar_data)
        self.make_radar_chart(self.ax2, "Input keyowords", 222, self.polar_data)
        self.make_bar_chart(self.ax3, self.bar_data, "Hello title")
        self.make_time_chart(self.ax4, self.past_data, self.past_data2, "Past emotional status")

        return self.fig

    def make_radar_chart(self, ax, title, position, polar_data):
        # Erstelle radar chart
        ax = plt.subplot(position, polar=True)
        ax.set_title(title)
        # Beschrifte die Achsen (x = der Kreis, y = die "Speichen"), ylim = limits der y-Achse
        plt.xticks(self.polar_angles[:-1], self.xticks_labels, color='grey', size=10)
        plt.yticks(self.yticks_positions, self.yticks_labels, color="grey", size=8)
        ax.set_ylim(0, 1)
        # Plot data und fülle die Fläche dazwischen aus
        ax.plot(self.polar_angles, polar_data, alpha=1)
        ax.fill(self.polar_angles, polar_data, color='blue', alpha=0.1)

    def make_bar_chart(self, ax, bar_data, title):
        ax.set_title(title)
        ax.set_ylim(0, 1)
        ax.bar(self.xticks_labels, bar_data, width=.4, color="blue")

    def make_time_chart(self, ax, past_data, past_data2, title):
        ax.set_title(title)
        ax.yaxis.tick_right()
        ax.set_ylim(0, 1)
        ax.set_xlim(-4, 0)
        ax.plot(past_data[0], past_data[1])
        ax.plot(past_data2[0], past_data2[1])

    def update_radar_chart(self, values):
        pass

    def old(self):
        # tutorial commands for using axes/suplots etc
        # Benutze diese Methode für polar-Diagramme
        # if method == 1:
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
        # self.ax1 = self.fig.add_subplot(221)
        # self.ax2 = self.fig.add_subplot(222)
        # self.ax3 = self.fig.add_subplot(223)
        # self.ax4 = self.fig.add_subplot(224)

        # elif method == 2:
        # Den ganzen oberen Teil kann man auch einfacher haben:
        # Dabei werden die axes dem fig automatisch hinzugefügt
        #### self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(nrows=2, ncols=2)
        # nrows, ncols muss der Struktur der axes in den klammern ensprechen.
        # self.fig, ((self.ax1, self.ax2, self.ax3), (self.ax4, self.ax4, self.ax4,)) = plt.subplots(nrows=2, ncols=3)

        # In most cases, add_subplot would be the prefered method to create axes for plots on a canvas.
        # Only in cases where exact positioning matters, add_axes might be useful.
        pass
