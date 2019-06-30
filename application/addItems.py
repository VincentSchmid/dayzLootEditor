from os import getcwd
from os.path import abspath
from os.path import join
from tkinter import *
from tkinter import ttk

try:
    from application import xmlParser, xmlWriter, windows
except ModuleNotFoundError:
    import xmlParser
    import windows
    import writeItemToXML


class addItems(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.wm_title("Paste types")
        self.window.grab_set()

        self.mods = windows.getMods()
        self.addInfoFrame = Frame(self.window)
        self.addInfoFrame.grid(row=2, pady=3, sticky="w")
        Label(self.addInfoFrame, text="Enter Mod name:").grid(row=0, column=0, padx=3, pady=3)
        self.modSelector = ttk.Combobox(self.addInfoFrame, values=self.mods)
        self.modSelector.grid(row=0, column=1)

        self.text = Text(self.window)
        self.text.grid(row=1, padx=3, pady=3)

        self.buttons = Frame(self.window)
        self.buttons.grid(row=3, sticky="w")
        Button(self.buttons, text="OK", height=1, width=10, command=self.confirm)\
            .grid(padx=10, pady=10)

        windows.center(self.window)

    def confirm(self):
        selectedMod = self.modSelector.get()
        if selectedMod == "":
            selectedMod = self.mods[0]

        text = self.text.get(1.0, END).strip()

        err = xmlParser.checkIfTypesXML(text)
        if err == 1:
            windows.showError(self.window, "Beginning of type is wrong", "type has to start with <type ")

        if err == 2:
            windows.showError(self.window, "End of type is wrong", "Ending is wrong,\n"
                                                                   "Block possibly not closed")
        if err == 0:
            if text.startswith("<type"):
                types = "<types>\n  " + text + "\n</types>"
        #Outsource this to own logic
            windows.appendTypesToDatabase(types, self.window, selectedMod)



def testWindow():
    window = Tk()
    addItems(window)
    window.mainloop()