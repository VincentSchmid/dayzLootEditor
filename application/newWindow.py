from tkinter import *
from tkinter import ttk

try:
    from application import xmlParser, xmlWriter, windows
except ModuleNotFoundError:
    import xmlParser
    import windows
    import writeItemToXML


class newWindow(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.wm_title("Window name")
        self.window.grab_set()

        self.exampleFrame = Frame(self.window)
        self.exampleFrame.grid()

        windows.center(self.window)


def testWindow():
    window = Tk()
    newWindow(window)
    window.mainloop()

testWindow()