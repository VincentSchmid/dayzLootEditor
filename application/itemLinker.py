from tkinter import *
from tkinter import ttk


import xmlParser
import windows
import xmlWriter
import dao


class itemLinker(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.wm_title("Item Linker")
        self.window.grab_set()

        self.mods = ["All Mods"]
        self.mods.extend(windows.getMods())
        self.items = []
        self.listBoxes = []
        self.searchEntries = []
        self.categoryEntries = []
        self.modEntries = []

        self.topRow = Frame(self.window)
        self.topRow.grid(sticky="w")

        self.mainArea = Frame(self.window)
        self.mainArea.grid(row=1, column=0, sticky="ns")

        self.createMainArea()

        self.windowButtons = Frame(self.window)
        self.windowButtons.grid(row=2)

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.fillBoxes()

        windows.center(self.window)

    def createMainArea(self):
        self.parentFrame = Frame(self.mainArea)
        self.parentFrame.grid(row=1, column=0, sticky="ns")
        self.createItemSelector(self.parentFrame, "Parent", 0)

        self.allItemFrame = Frame(self.mainArea)
        self.allItemFrame.grid(row=1, column=1, sticky="ns")
        self.createItemSelector(self.allItemFrame, "All Items", 1)

        self.linkbttnFrame = Frame(self.mainArea)
        self.linkbttnFrame.grid(row=1, column=2)
        Button(self.linkbttnFrame, text=">>", height=3, width=3, command=self.addLink) \
            .grid(padx=10, pady=10)
        Button(self.linkbttnFrame, text="<<", height=3, width=3, command=self.removeLink) \
            .grid(row=1, padx=10, pady=10)

        self.linkedFrame = Frame(self.mainArea)
        self.linkedFrame.grid(row=1, column=3, sticky="ns")
        self.createItemSelector(self.linkedFrame, "Linked Items", 3)

        self.listBoxes[0].bind('<<ListboxSelect>>', self.getLinks)

        self.categoryEntries[-1][0].grid_forget()
        self.categoryEntries[-1][1].grid_forget()
        self.modEntries[-1][0].grid_forget()
        self.modEntries[-1][1].grid_forget()
        self.searchEntries[-1][1].grid_forget()
        self.searchEntries[-1][2].grid_forget()

    def createItemSelector(self, root, frameName, col):
        lFrame = LabelFrame(root, text=frameName)
        lFrame.grid(padx=5, sticky="ns")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)


        listboxFrame = Frame(lFrame)
        listboxFrame.grid(row=1, padx=5, sticky="ns")

        lFrame.grid_rowconfigure(1, weight=1)
        lFrame.grid_columnconfigure(0, weight=1)


        lb = Listbox(listboxFrame, width=35, height=30, exportselection=False)
        lb.grid(sticky="ns")
        self.listBoxes.append(lb)

        listboxFrame.grid_rowconfigure(0, weight=1)
        listboxFrame.grid_columnconfigure(0, weight=1)

        sb1 = Scrollbar(listboxFrame)
        sb1.grid(row=0, column=1, sticky="n,s")
        lb.config(yscrollcommand=sb1.set)
        sb1.config(command=lb.yview)

        toolsFrame = Frame(lFrame)
        toolsFrame.grid(row=2, sticky="w", pady=4)

        sl = Label(toolsFrame, text="search")
        sl.grid(row=1, padx=5, sticky="w")
        cat = Label(toolsFrame, text="category")
        cat.grid(row=2, padx=5, sticky="w")

        name = StringVar()
        entry = Entry(toolsFrame, textvariable=name, width=23)
        entry.grid(row=1, column=1, pady=4, sticky="w")
        name.trace("w", self.search)
        self.searchEntries.append((name, sl, entry))

        category = ttk.Combobox(toolsFrame, values=xmlParser.selection, width=20)
        category.grid(row=2, column=1, pady=4, sticky="w")
        category.bind("<<ComboboxSelected>>", self.updateView)
        category.current(len(xmlParser.selection)-1)
        self.categoryEntries.append((cat, category))

        ml = Label(toolsFrame, text="Mod")
        ml.grid(row=3, padx=5, sticky="w")

        modSelector = ttk.Combobox(toolsFrame, values=self.mods)
        modSelector.grid(row=3, column=1, pady=4, sticky="w")
        modSelector.bind("<<ComboboxSelected>>", self.updateView)
        modSelector.current(0)
        self.modEntries.append((ml, modSelector))

    def addLink(self):
        dao.createCombos([(self.listBoxes[0].get(ANCHOR), self.listBoxes[1].get(ANCHOR))])
        self.getLinks()

    def removeLink(self):
        dao.removeCombo((self.listBoxes[0].get(ANCHOR), self.listBoxes[2].get(ANCHOR)))
        self.getLinks()

    def fillBoxes(self):
        all = [xmlParser.selection[-1], self.mods[0]]
        parentValues = [self.searchEntries[0][0].get(), self.modEntries[0][1].get(), self.categoryEntries[0][1].get()]
        allItemsValues = [self.searchEntries[1][0].get(), self.modEntries[1][1].get(), self.categoryEntries[1][1].get()]

        values = parentValues
        box = self.listBoxes

        rows = dao.getItemsFromCatMods(values[2], values[1], *all, values[0])
        windows.updateListBox(box[0], rows)

        values = allItemsValues

        rows = dao.getItemsFromCatMods(values[2], values[1], *all, values[0])
        windows.updateListBox(box[1], rows)


    def search(self, *args):
        all = [xmlParser.selection[-1], self.mods[0]]
        parentValues = [self.searchEntries[0][0].get(), self.modEntries[0][1].get(), self.categoryEntries[0][1].get()]
        allItemsValues = [self.searchEntries[1][0].get(), self.modEntries[1][1].get(), self.categoryEntries[1][1].get()]
        values = parentValues
        box = self.listBoxes[0]

        if self.window.focus_get() == self.searchEntries[1][2]:
            values = allItemsValues
            box = self.listBoxes[1]


        rows = dao.getItemsFromCatMods(values[2], values[1], *all, values[0])
        windows.updateListBox(box, rows)

    def updateView(self, event):
        #rough
        all = [xmlParser.selection[-1], self.mods[0]]
        parentWidgets = [self.searchEntries[0][2], self.modEntries[0][1], self.categoryEntries[0][1]]
        parentValues = [self.searchEntries[0][0].get(), self.modEntries[0][1].get(), self.categoryEntries[0][1].get()]
        allItemsWidgets = [self.searchEntries[1][2], self.modEntries[1][1], self.categoryEntries[1][1]]
        allItemsValues = [self.searchEntries[1][0].get(), self.modEntries[1][1].get(), self.categoryEntries[1][1].get()]

        values = parentValues
        box = self.listBoxes[0]

        if event.widget in parentWidgets:
            values = parentValues
            box = self.listBoxes[0]

        if event.widget in allItemsWidgets:
            values = allItemsValues
            box = self.listBoxes[1]

        rows = dao.getItemsFromCatMods(values[2], values[1], *all, values[0])
        windows.updateListBox(box, rows)

    def getLinks(self, event=None):
        self.listBoxes[2].delete(0, END)
        for item in dao.getLinkedItems(self.listBoxes[0].get(ANCHOR)):
            self.listBoxes[2].insert(END, item)



def testWindow():
    window = Tk()
    itemLinker(window)
    window.mainloop()