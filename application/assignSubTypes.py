from tkinter import *


import xmlParser
import windows
import xmlWriter


class newWindow(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.wm_title("Trader")
        self.window.grab_set()

        self.main = Frame(self.window)
        self.main.grid()

        windows.center(self.window)

    def createSubTypes(self):
        subtypesFrame = Frame(self.main)
        lb = Listbox(subtypesFrame, width=35, height=30, exportselection=False)
        lb.grid(sticky="ns")

    def createTraderEditor(self):
        pass


def testWindow():
    window = Tk()
    newWindow(window)
    window.mainloop()


testWindow()