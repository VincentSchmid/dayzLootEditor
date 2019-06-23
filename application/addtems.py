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
        self.window.grab_set()

        self.text = Text(self.window)
        self.text.grid(padx=3, pady=3)
        self.buttons = Frame(self.window)
        self.buttons.grid(row=1)
        Button(self.buttons, text="OK", height=1, width=10, command=self.confirm).grid(padx=10, pady=10)

    def confirm(self):
        #text = self.text.get(1.0, END).strip()
        text = """<type name="ACOGOptic">
    <nominal>5</nominal>
    <lifetime>1800</lifetime>
    <restock>1800</restock>
    <min>3</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="1" />
    <category name="weapons" />
    <usage name="Military" />
  </type>
  <type name="AgaricusMushroom">
    <lifetime>900</lifetime>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="1" deloot="0" />
  </type>
  <type name="AK74_Hndgrd">
    <nominal>6</nominal>
    <lifetime>7200</lifetime>
    <restock>0</restock>
    <min>2</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0" />
    <category name="weapons" />
    <usage name="Military" />
  </type>"""

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
                print("yay")
                text = "<types>\n\t" + text + "\n</types>"

            items = xmlParser.parseFromString(text)
            print(items)



window = Tk()
addItems(window)

window.mainloop()