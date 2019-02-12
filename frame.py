import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
matplotlib.use('TkAgg')

class Frame:
    def __init__(self, chatbot_name, bot, character, init_emotional_state, init_emotional_history):
        # initialise variables
        self.chatbot_name = chatbot_name
        self.bot = bot
        self.character = character
        self.user_input = None
        # saves what diagrams are displayable, which are active and what type they are
        self.visible_diagrams = {
            "emotional_state": [True, "bar"],
            "emotional_history": [True, "time"],
            "input_emotions": [False, "bar"],
            "input_topics": [False, "bar"]
        }

        self.dgm = DiagramManager(self.visible_diagrams, init_emotional_state, init_emotional_history)
        # initialize all ui elements
        self.root = tk.Tk()
        self.menubar = tk.Menu(self.root)
        self.menu = tk.Menu(self.menubar, tearoff=0)
        self.chat_out = tk.Text(self.root, width=40, state="disabled")
        self.chat_in = tk.Entry(self.root)
        self.log = tk.Text(self.root, width=40, state="disabled")
        self.info_label = tk.Label(self.root, text="EIKA v.0.0.1, cMarcel Müller, FH Dortmund ")
        self.send_button = tk.Button(self.root, text="Send", command=self.notify_controller_proxy)
        self.diagram_frame = tk.Frame(self.root)
        self.diagram_canvas = FigureCanvas(self.dgm.get_diagrams(), master=self.diagram_frame)
        self.chat_in.bind('<Return>', self.notify_subscribers)
        self.chat_in.focus_set()

        # create frame and menu
        self.create_frame(self.chatbot_name)
        self.pack_widgets()

        # set subscriber list (implements observer pattern)
        self.controller = None
        self.subscribers = set()

    # creates main frame and menu bar
    def create_frame(self, title):
        # create menubar entries
        self.menu.add_command(label="Update canvas", command=self.update_diagrams)
        self.menu.add_separator()
        self.menu.add_command(label="Retrain chatbot", command=self.bot.train)
        self.menu.add_command(label="Reset chatbot", command=self.reset_bot)
        self.menu.add_command(label="Change name", command=self.show_name_window)
        self.menubar.add_cascade(label="Configure", menu=self.menu)
        # create root-window
        self.root.configure(menu=self.menubar)
        self.root.title(title)
        self.root.resizable(0, 0)

    # places widgets in the frame
    def pack_widgets(self):
        # position ui elements
        self.chat_out.grid(row=1, column=1, columnspan=2, sticky=tk.E + tk.W + tk.N + tk.S)
        self.log.grid(row=1, column=3, sticky=tk.E + tk.W + tk.N + tk.S)
        self.chat_in.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.send_button.grid(row=2, column=2, sticky=tk.E + tk.W)
        self.diagram_frame.grid(row=1, column=4, columnspan=2, sticky=tk.E + tk.W + tk.N + tk.S)
        self.info_label.grid(row=2, column=4, sticky=tk.E)
        self.diagram_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # TODO diese methoden so ausbauen, dass man damit alle werte des charackters ändern kann
    def show_name_window(self):
        self.change_name_frame = tk.Tk()

        self.name_label = tk.Label(self.change_name_frame, text="Enter name below and confim with enter")
        self.namein = tk.Entry(self.change_name_frame)
        self.namein.bind('<Return>', self.change_name)

        self.name_label.pack()
        self.namein.pack()

        self.change_name_frame.mainloop()

    def change_name(self, event):
        self.new_name = self.namein.get()
        print(self.new_name)
        self.change_name_frame.destroy()

    # TODO Methode, mit der man auswählen kann welche Diagramme man sehen will
    # Beispieldiagramme:
    # emotional_state des bots
    # emotional_history des bots
    # input message emotions
    # input topics

    # the following two function implement the observer pattern
    def register(self, who):
        # Set of subscribers, there should only ever be the controller in there
        self.subscribers.add(who)
        # Controller class, only class this one here is allowed to talk to
        self.controller = who

    # Delays a command to the notify_controller from objects that cant pass an event (like the button)
    def notify_controller_proxy(self):
        self.notify_subscribers(None)

    # notifies objects that are observing this class
    def notify_subscribers(self, event):
        self.user_input = self.chat_in.get()
        if self.user_input:
            self.controller.handle_input(self.user_input)

    # prints in chatout widget
    def update_chat_out(self, input, response):
        # prints input, empties input field
        self.chat_out.configure(state="normal")
        self.chat_out.insert(tk.END, "Du: " + input + "\n")
        # deletes text from index 0 till the end in input filed
        self.chat_in.delete(0, tk.END)
        # inserts chatbot answer in chat
        self.chat_out.insert(tk.END, self.chatbot_name + ": " + response + "\n")
        self.chat_out.see(tk.END)
        self.chat_out.configure(state="disabled")

    # prints to the log widget, used to display additional text data (sentiment etc)
    def update_log(self, output):
        # unlock widget, insert, lock widget
        self.log.configure(state="normal")
        self.log.delete(1.0, tk.END)
        for item in output:
            self.log.insert(tk.END, item + "\n")
        self.log.configure(state="disabled")

    # updates diagrams with new values
    def update_diagrams(self, emotional_state, history_data):
        self.dgm.update_time_chart(history_data, self.diagram_canvas)
        self.dgm.update_bar_chart(self.dgm.ax3, emotional_state, history_data, self.diagram_canvas)

    # resets bit to default values and updates the diagrams
    def reset_bot(self):
        self.character.set_to_defaults()
        self.update_diagrams(self.character.get_emotional_state(), self.character.get_emotional_history())

    def show(self):
        self.root.mainloop()

# TODO hier die methode so modifizieren, dass die diagramme nach dem dict "visible_diagrams" aufgebaut werden
class DiagramManager:
    def __init__(self, diagrams, init_emotional_state, init_emotional_history):
        # Data that is needed to make the diagrams (labels, ticks, colors, etc)
        self.polar_angles = [n / float(5) * 2 * np.pi for n in range(5)]
        self.polar_angles += self.polar_angles[:1]
        self.polar_chart_yticks_positions = [0.2, 0.4, 0.6, 0.8]
        self.polar_chart_yticks_labels = [".2", ".4", ".6", ".8"]
        self.time_chart_x_values = [0, -1, -2, -3, -4]
        self.labels = []
        self.plot_colors = ["orange", "grey", "red", "blue", "green"]
        self.plot_colors_previous_step = ["black", "black", "black", "black", "black"]
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

        # TODO hier damit ansetzen (siehe letztes todo)
        # create diagrams according to the visible diagrams
        self.make_bar_chart(self.ax3, init_emotional_state, init_emotional_history, "bot emotional state")
        self.make_time_chart(self.ax4, init_emotional_history, "bot emotional state history")
        self.fig.set_tight_layout(True)

    def get_diagrams(self):
        return self.fig

    # create and update a bar chart
    def make_bar_chart(self, ax, init_bar_data, history_data, title):
        ax.set_title(title)
        ax.set_ylim(0, 1)
        ax.yaxis.tick_right()
        ax.grid(axis="y", linestyle=':', linewidth=.5)

        self.labels.clear()
        for index in range(len(self.plot_classes)):
            self.labels.append(self.plot_classes[index] + " (" + init_bar_data[index].__str__() + ")")

        ax.bar(self.labels, init_bar_data, width=.9, color=self.plot_colors, alpha=.75)
        ax.bar(self.labels, history_data[1], width=.01, color=self.plot_colors_previous_step, alpha=1)

    def update_bar_chart(self, ax, emotional_state, history_data, canvas):

        ax.clear()
        self.make_bar_chart(ax, emotional_state, history_data, "bot emotional state")
        canvas.draw()

    # create and update a line chart
    def make_time_chart(self, ax, init_time_data, title):
        ax.set_title(title)
        ax.yaxis.tick_right()
        ax.set_xlim(-4, 0)
        ax.set_xticks(np.arange(-4, 0, 1))
        ax.set_ylim(0, 1)
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

