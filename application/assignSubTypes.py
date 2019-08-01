from tkinter import *
from tkinter import ttk


import xmlParser
import windows
import xmlWriter
import dao
import scrolledWindow


class newWindow(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.wm_title("Trader")
        self.window.grab_set()

        self.traderVal = []

        self.main = Frame(self.window)
        self.main.grid()

        self.createSubTypes()
        self.createTraderEditor(self.window, 0, 1, [])
        self.subTypeListbox.bind("<<ListboxSelect>>", self.fillTraderWindow)

        windows.center(self.window)

    def createSubTypes(self):
        subtypesFrame = Frame(self.main)
        subtypesFrame.grid()
        self.subTypeListbox = Listbox(subtypesFrame, width=35, height=30, exportselection=False)
        self.subTypeListbox.grid(sticky="ns")
        subTypes = dao.getSubtypes()
        for subType in subTypes:
            if subType == "":
                subType = "UNASSIGNED"
            self.subTypeListbox.insert(END, subType)

    def createTraderEditor(self, root, row, column, rows):
        self.frame = Frame(root, height=450, bg="#EBEBEB")
        self.frame.grid(row=row, column=column, sticky="nw")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.canv = Canvas(self.frame, height=450, bg="#EBEBEB")
        self.canv.grid(row=0, column=0, sticky="nsew")

        self.canvFrame = Frame(self.canv, height=450, bg="#EBEBEB")
        self.canv.create_window(0, 0, window=self.canvFrame, anchor='nw')

        for item in rows:
            self.traderRow(self.canvFrame, *item)

        scrl = Scrollbar(self.frame, orient=VERTICAL)
        scrl.config(command=self.canv.yview)
        self.canv.config(yscrollcommand=scrl.set)
        scrl.grid(row=0, column=1, sticky="ns")

        root.rowconfigure(row, weight=1)
        root.columnconfigure(column, weight=1)

        self.canvFrame.bind("<Configure>", self.update_scrollregion)

    def update_scrollregion(self, event):
        self.canv.configure(scrollregion=self.canv.bbox("all"))

    def traderRow(self, parent, name, traderCat, buyPrice, sellPrice):
        frame = Frame(parent)
        frame.grid(padx=10, pady=10, sticky="w")

        nameVar = StringVar()
        nameVar.set(name)

        traderCatVar = StringVar()
        traderCatVar.set(traderCat)

        buyPriceVar = StringVar()
        buyPriceVar.set(buyPrice)

        sellPriceVar = StringVar()
        sellPriceVar.set(sellPrice)

        xpad = 10

        entry1 = Entry(frame, textvariable=nameVar, width=25)
        entry1.grid(row=0, column=0, padx=xpad)
        entry2 = Entry(frame, textvariable=traderCatVar, width=3)
        entry2.grid(row=0, column=1, padx=xpad)
        entry3 = Entry(frame, textvariable=buyPriceVar, width=8)
        entry3.grid(row=0, column=2, padx=xpad)
        entry4 = Entry(frame, textvariable=sellPriceVar, width=8)
        entry4.grid(row=0, column=3, padx=xpad)

        self.traderVal.append(([traderCatVar, buyPriceVar, sellPriceVar], [frame, entry1, entry2, entry3, entry4]))

    def clearTraderWindow(self):
        self.frame.grid_forget()

        self.traderVal = []

    def fillTraderWindow(self, event):
        self.clearTraderWindow()
        selSubtype = self.subTypeListbox.get(ANCHOR)
        print(selSubtype)

        itemsOfSubtype = dao.getSubtypeForTrader(selSubtype)

        self.createTraderEditor(self.window, 0, 1, itemsOfSubtype)


def testWindow():
    window = Tk()
    newWindow(window)
    window.mainloop()


testWindow()