# If you import somemodule the contained globals will be available via somemodule.someglobal. If you from somemodule import * ALL its globals
# (or those listed in __all__ if it exists) will be made globals, i.e. you can access them using someglobal without the module name in front of it.
# Using from module import * is discouraged as it clutters the global scope and if you import stuff from multiple modules you are likely to get
# conflicts and overwrite existing classes/functions.

import tkinter
import tkinter.ttk #provides access to the Tk themed widget set

rootWindow = tkinter.Tk()
rootWindow.title("EIKA")



#tkinter.ttk.Button(rootWindow, text="button").grid()
#tkinter.Button(rootWindow, text="hi").grid()

topFrame = tkinter.Frame(rootWindow)
bottomFrame = tkinter.Frame(rootWindow)

button1 = tkinter.Button(topFrame, text="Button1", fg="red") #fg=foreground color, d.h. die textfarbe
button2 = tkinter.Button(topFrame, text="Button2", fg="blue")
button3 = tkinter.Button(topFrame, text="Button3", fg="green") #fg=foreground color, d.h. die textfarbe
button4 = tkinter.Button(bottomFrame, text="Button4", fg="purple", bg="blue")





topFrame.pack(side=tkinter.TOP) #pack packt das element einfach in rootWindow, ohne Layout, geht nicht wenn da schon ein element in einem layout drin ist
bottomFrame.pack(side=tkinter.BOTTOM)

button1.pack(side=tkinter.LEFT) #left packt das Element so weit nach links wie möglich
button2.pack(side=tkinter.LEFT)
button3.pack(side=tkinter.LEFT)
button4.pack(side=tkinter.LEFT)






rootWindow.mainloop()