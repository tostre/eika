import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
matplotlib.use('TkAgg')

class Frame:
    def __init__(self, cb_name, bot, init_emotional_state, init_emotional_history):
        # initialise variables
        self.cb_name = cb_name
        self.bot = bot
        self.user_input = None
        self.response = None
        self.root = tk.Tk()
        self.dgm = DiagramManager(init_emotional_state, init_emotional_history)

        # create menubar
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Edit bot personality")
        self.filemenu.add_command(label="Edit bot mood")
        self.filemenu.add_command(label="Edit bot emotions")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Retrain chatbot", command=self.bot.train)
        self.filemenu.add_command(label="Update canvas", command=self.update_diagrams)
        self.menubar.add_cascade(label="Configure", menu=self.filemenu)

        # create root-window
        self.root.configure(menu=self.menubar)
        self.root.title(cb_name)
        self.root.resizable(0, 0)

        # create widgets
        self.chatout = tk.Text(self.root, width=60, state="disabled")
        self.chatin = tk.Entry(self.root)
        self.chatin.bind('<Return>', self.notify_controller)
        self.chatin.focus_set()
        self.log = tk.Text(self.root, width=30, state="disabled")
        self.info_label = tk.Label(self.root, text="EIKA v.0.0.1, cMarcel Müller, FH Dortmund ")
        self.button = tk.Button(self.root, text="Send", command=self.notify_controller_proxy)

        # create diagram space
        self.diagram_frame = tk.Frame(self.root)
        self.diagram_canvas = FigureCanvas(self.dgm.get_diagrams(), master=self.diagram_frame)

        # position ui elements
        self.chatout.grid(row=1, column=1, columnspan=2, sticky=tk.E + tk.W + tk.N + tk.S)
        self.log.grid(row=1, column=3, sticky=tk.E + tk.W + tk.N + tk.S)
        self.chatin.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.button.grid(row=2, column=2, sticky=tk.E + tk.W)
        self.diagram_frame.grid(row=1, column=4, columnspan=2, sticky=tk.E + tk.W + tk.N + tk.S)
        self.info_label.grid(row=2, column=4, sticky=tk.E)
        self.diagram_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # set subscriber list (implements observer pattern)
        self.controller = None
        self.subscribers = set()

    # the following two function implement the observer pattern
    def register(self, who):
        # Set of subscribers, there should only ever be the controller in there
        self.subscribers.add(who)
        # Controller class, only class this one here is allowed to talk to
        self.controller = who

    # Delays a command to the notify_controller from objects that cant pass an event (like the button)
    def notify_controller_proxy(self):
        self.notify_controller(None)

    def notify_controller(self, event):
        self.user_input = self.chatin.get()
        if self.user_input:
            self.controller.handle_input(self.user_input)

    # prints in chatout widget
    def update_chatout(self, input, response):
        # prints input, empties input field
        self.chatout.configure(state="normal")
        self.chatout.insert(tk.END, "Du: " + input + "\n")
        # deletes text from index 0 till the end in input filed
        self.chatin.delete(0, tk.END)
        # inserts chatbot answer in chat
        self.chatout.insert(tk.END, self.cb_name + ": " + response + "\n")
        self.chatout.see(tk.END)
        self.chatout.configure(state="disabled")

    # prints to the log widget, used to display additional text data (sentiment etc)
    def update_log(self, output):
        # unlock widget, insert, lock widget
        self.log.configure(state="normal")
        self.log.delete(1.0, tk.END)
        for item in output:
            self.log.insert(tk.END, item + "\n")
        self.log.configure(state="disabled")

    def update_diagrams(self, emotional_state, history_data):
        self.dgm.update_time_chart(history_data, self.diagram_canvas)
        self.dgm.update_bar_chart(self.dgm.ax3, emotional_state, self.diagram_canvas)

    def show(self):
        self.root.mainloop()


class DiagramManager:
    def __init__(self, init_emotional_state, init_emotional_history):
        # Data that is needed to make the diagrams (labels, ticks, colors, etc)
        self.polar_angles = [n / float(5) * 2 * np.pi for n in range(5)]
        self.polar_angles += self.polar_angles[:1]
        self.polar_chart_yticks_positions = [0.2, 0.4, 0.6, 0.8]
        self.polar_chart_yticks_labels = [".2", ".4", ".6", ".8"]
        self.time_chart_x_values = [0, -1, -2, -3, -4]
        self.labels = []
        self.plot_colors = ["orange", "grey", "red", "blue", "green"]
        self.plot_classes = ["hap", "sad", "ang", "fea", "dis"]

        # 2D-lines that depict the development of the emotional state
        self.time_plot1, self.time_plot2, self.time_plot3, self.time_plot4, self.time_plot5 = (None, None, None, None, None)
        self.polar_plot = None
        self.bar_plot = None

        # init figure and subplots/axes
        self.fig = matplotlib.figure.Figure()
        self.ax3 = self.fig.add_subplot(211)
        self.ax4 = self.fig.add_subplot(212)
        # self.make_radar_chart(self.ax1, "Input emotions", 221, self.init_polar_data)
        # self.make_radar_chart(self.ax2, "Input keywords", 222, self.init_polar_data)
        self.make_bar_chart(self.ax3, init_emotional_state, "bot emotional state")
        self.make_time_chart(self.ax4, init_emotional_history, "bot emotional state history")
        self.fig.set_tight_layout(True)

    def get_diagrams(self):
        return self.fig

    # create and update a bar chart
    def make_bar_chart(self, ax, init_bar_data, title):
        ax.set_title(title)
        ax.set_ylim(0, 1)
        ax.yaxis.tick_right()
        ax.grid(axis="y", linestyle=':', linewidth=.5)

        self.labels.clear()
        for index in range(len(self.plot_classes)):
            self.labels.append(self.plot_classes[index] + " (" + init_bar_data[index].__str__() + ")")

        ax.bar(self.labels, init_bar_data, width=.9, color=self.plot_colors, alpha=.75)

    def update_bar_chart(self, ax, emotional_state, canvas):
        ax.clear()
        self.make_bar_chart(ax, emotional_state, "bot emotional state")
        canvas.draw()

    # create and update a line chart
    def make_time_chart(self, ax, init_time_data, title):
        ax.set_title(title)
        ax.yaxis.tick_right()
        ax.set_ylim(0, 1)
        ax.set_xlim(-4, 0)
        ax.grid(axis="y", linestyle=':', linewidth=.5)
        # Graphen plotten
        self.time_plot1, = ax.plot(self.time_chart_x_values, [init_time_data[i][0] for i in range(0, 5)], linewidth=.5, color=self.plot_colors[0])
        self.time_plot2, = ax.plot(self.time_chart_x_values, [init_time_data[i][1] for i in range(0, 5)], linewidth=.5, color=self.plot_colors[1])
        self.time_plot3, = ax.plot(self.time_chart_x_values, [init_time_data[i][2] for i in range(0, 5)], linewidth=.5, color=self.plot_colors[2])
        self.time_plot4, = ax.plot(self.time_chart_x_values, [init_time_data[i][3] for i in range(0, 5)], linewidth=.5, color=self.plot_colors[3])
        self.time_plot5, = ax.plot(self.time_chart_x_values, [init_time_data[i][4] for i in range(0, 5)], linewidth=.5, color=self.plot_colors[4])
        # Legende erstellen
        ax.legend((self.time_plot1, self.time_plot2, self.time_plot3, self.time_plot4, self.time_plot5), self.plot_classes, loc=2)

    def update_time_chart(self, time_data, diagram_canvas):
        self.time_plot1.set_ydata([time_data[i][0] for i in range(0, 5)])
        self.time_plot2.set_ydata([time_data[i][1] for i in range(0, 5)])
        self.time_plot3.set_ydata([time_data[i][2] for i in range(0, 5)])
        self.time_plot4.set_ydata([time_data[i][3] for i in range(0, 5)])
        self.time_plot5.set_ydata([time_data[i][4] for i in range(0, 5)])
        diagram_canvas.draw()

    # create and update a radar chart
    def make_radar_chart(self, ax, title, position, polar_data):
        # Erstelle radar chart
        ax = plt.subplot(position, polar=True)
        ax.set_title(title)
        # Beschrifte die Achsen (x = der Kreis, y = die "Speichen"), ylim = limits der y-Achse
        plt.xticks(self.polar_angles[:-1], self.plot_classes, color='grey', size=10)
        plt.yticks(self.polar_chart_yticks_positions, self.polar_chart_yticks_labels, color="grey", size=8)
        ax.set_ylim(0, 1)
        # Plot data und fülle die Fläche dazwischen aus
        self.polar_plot, = ax.plot(self.polar_angles, polar_data, alpha=1, linewidth=5)
        ax.fill(self.polar_angles, polar_data, color='blue', alpha=0.1)

    def update_radar_chart(self, new_data, canvas):
        new_data[0].append(new_data[0][0])
        new_data[1].append(new_data[1][0])
        self.polar_plot.set_data(new_data[0], new_data[1])
        self.polar_plot.set_xdata(new_data[0])
        canvas.draw()

    # old methods
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

    # hier wird die plt.Figure benutzt statt die matplotbib-figure. Die wird aber nicht richtig beendet, wenn das Fenster geschlossen wird
    def __init2(self, init_emotional_state, init_emotional_history):
        # Data that is needed to make the diagrams (labels, ticks, colors, etc)
        self.polar_angles = [n / float(5) * 2 * np.pi for n in range(5)]
        self.polar_angles += self.polar_angles[:1]
        self.polar_chart_yticks_positions = [0.2, 0.4, 0.6, 0.8]
        self.polar_chart_yticks_labels = [".2", ".4", ".6", ".8"]
        self.time_chart_x_values = [0, -1, -2, -3, -4]
        self.plot_colors = ["orange", "grey", "red", "blue", "green"]
        self.plot_classes = ["hap", "sad", "ang", "fea", "dis"]

        # 3D-lines that depict the development of the emotional state
        self.time_plot1, self.time_plot2, self.time_plot3, self.time_plot4, self.time_plot5 = (None, None, None, None, None)
        self.polar_plot = None
        self.bar_plot = None

        # init figure and subplots/axes
        self.fig, (self.ax3, self.ax4) = plt.subplots(nrows=2, ncols=1)
        #self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(nrows=2, ncols=2)
        # self.make_radar_chart(self.ax1, "Input emotions", 221, self.init_polar_data)
        # self.make_radar_chart(self.ax2, "Input keywords", 222, self.init_polar_data)
        self.make_bar_chart(self.ax3, init_emotional_state, "bot emotional state")
        self.make_time_chart(self.ax4, init_emotional_history, "bot emotional state history")
        self.fig.tight_layout()