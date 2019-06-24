from os import getcwd
from os.path import abspath
from os.path import join
from tkinter import *

try:
    from application import xmlParser, writeItemToXML, windows
except ModuleNotFoundError:
    import xmlParser
    import windows
    import writeItemToXML


class addItems(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.wm_title("Paste types")
        self.window.grab_set()

        self.text = Text(self.window)
        self.text.grid(padx=3, pady=3)
        self.buttons = Frame(self.window)
        self.buttons.grid(row=1)
        Button(self.buttons, text="OK", height=1, width=10, command=self.confirm).grid(padx=10, pady=10)

        windows.center(self.window)

    def confirm(self):
        text = self.text.get(1.0, END).strip()

        # returns 1 if beginning wrong
        # returns 2 if end wrong
        # returns 0 if good
        err = xmlParser.checkIfTypesXML(text)
        if err == 1:
            windows.showError(self.window, "Beginning of type is wrong", "type has to start with <type ")

        if err == 2:
            windows.showError(self.window, "End of type is wrong", "Ending is wrong,\n"
                                                                   "Block possibly not closed")
        if err == 0:
            if text.startswith("<type"):
                types = "<types>\n\t" + text + "\n</types>"

            newItemNames = windows.appendTypesToDatabase(types, self.window)
            text = text.split("</type>")
            toAppend = []
            for itemName in newItemNames:
                for type in text:
                    if itemName in type.split(">")[0]:
                        toAppend.append(type + "</type>")

            windows.appendtoSorce(toAppend)


def testWindow():
    window = Tk()
    addItems(window)
    window.mainloop()