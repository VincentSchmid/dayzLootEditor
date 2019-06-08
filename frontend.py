from tkinter import *
from tkinter import ttk
import dao
import XMLtypes
import xmlParsing4

itemTypes = ["gun", "ammo", "optic", "mag", "attachment"]


class Window(object):
    def __init__(self, window):
        self.window = window
        self.window.wm_title("Loot Editor v0.1")

        entryFrame = Frame(self.window)
        entryFrame.grid(row=0, column=0, sticky="n,w,e")

        l1 = Label(entryFrame, text="name")
        l1.grid(row=0, column=0)

        l2 = Label(entryFrame, text="nominal")
        l2.grid(row=0, column=2)

        l3 = Label(entryFrame, text="min")
        l3.grid(row=0, column=4)

        l5 = Label(entryFrame, text="restock")
        l5.grid(row=0, column=6)

        l4 = Label(entryFrame, text="lifetime")
        l4.grid(row=0, column=8)

        self.name_text = StringVar()
        self.nameEntry = Entry(entryFrame, textvariable=self.name_text)
        self.nameEntry.grid(row=0, column=1)

        self.nominal_text = StringVar()
        self.nominalEntry = Entry(entryFrame, textvariable=self.nominal_text)
        self.nominalEntry.grid(row=0, column=3)

        self.min_text = StringVar()
        self.minEntry = Entry(entryFrame, textvariable=self.min_text)
        self.minEntry.grid(row=0, column=5)

        self.restock_text = StringVar()
        self.restockEntry = Entry(entryFrame, textvariable=self.restock_text)
        self.restockEntry.grid(row=0, column=7)

        self.lifetime_text = StringVar()
        self.lifetimeEntry = Entry(entryFrame, textvariable=self.lifetime_text)
        self.lifetimeEntry.grid(row=0, column=9)

        # Set the treeview
        self.tree = ttk.Treeview(self.window,
                                 columns=('name', 'nominal', 'min', 'restock', 'lifetime'))
        self.tree.heading('#0', text='name')
        self.tree.heading('#1', text='nominal')
        self.tree.heading('#2', text='min')
        self.tree.heading('#3', text='restock')
        self.tree.heading('#4', text='lifetime')
        self.tree.column('#1', stretch=YES)
        self.tree.column('#2', stretch=YES)
        self.tree.column('#0', stretch=YES)
        self.tree.column('#3', stretch=YES)
        self.tree.grid(row=4, rowspan=4, columnspan=10, sticky='nsew')
        self.treeview = self.tree
        self.tree.bind('<ButtonRelease-1>', self.fillEntryBoxes)
        
        self.window.grid_rowconfigure(4, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        sb1 = Scrollbar(window)
        sb1.grid(row=3, rowspan=4, column=11, sticky="n,s")
        self.tree.config(yscrollcommand=sb1.set)
        sb1.config(command=self.tree.yview)

        self.tkvar = StringVar(window)
        # todo get from backend
        choices = {'gun', 'mag', 'optic', 'attachment', "ammo", 'weapons'}
        self.tkvar.set('gun')  # set the default option

        b5 = Button(entryFrame, text="update sel", width=12, command=self.updateSel)
        b5.grid(row=0, column=12)

        buttons = Frame(self.window, width=200, height=150)
        buttons.grid(row=4, column=12, sticky="n")

        popupMenu = OptionMenu(buttons, self.tkvar, *choices)
        popupMenu.grid(row=0, column=0)

        b2 = Button(buttons, text="view type", width=12, command=self.viewType)
        b2.grid(row=1, column=0)

        b3 = Button(buttons, text="view linked items", width=12, command=self.viewCorresp)
        b3.grid(row=3, column=0)

        b4 = Button(buttons, text="search by name", width=12, command=self.searchByName)
        b4.grid(row=5, column=0)

        b6 = Button(buttons, text="update XML", width=12, command=self.updateXML)
        b6.grid(row=7, column=0)

        b7 = Button(buttons, text="close", width=12, command=window.destroy)
        b7.grid(row=9, column=0)

        self.infoFrame = Frame(self.window)
        self.infoFrame.grid(row=10, column=0, sticky="s,w,e")

        self.nomVars = []
        self.deltaNom = []
        self.startNominals = []
        self.createNominalVar()

    def createNominalVar(self):
        i = 1

        label = Label(self.infoFrame, text="overall nominal / delta:")
        label.grid(row=0, column=0)

        for type in itemTypes:
            var = StringVar()
            deltaStart = StringVar()

            self.startNominals.append(dao.getNominalByType(type))
            var.set(dao.getNominalByType(type))
            self.nomVars.append(var)
            deltaStart.set(0)
            self.deltaNom.append(deltaStart)

            label = Label(self.infoFrame, text=type + ":")
            label.grid(row=0, column=i)

            label = Label(self.infoFrame, textvariable=var)
            label.grid(row=0, column=i + 1)

            label = Label(self.infoFrame, text="/")
            label.grid(row=0, column=i + 2)

            label2 = Label(self.infoFrame, textvariable=deltaStart)
            label2.grid(row=0, column=i + 3)

            i += 4

    def updateNomVars(self):
        for i in range(len(self.nomVars)):
            nominal = dao.getNominalByType(itemTypes[i])
            self.nomVars[i].set(nominal)
            self.deltaNom[i].set(nominal - self.startNominals[i])

    def viewType(self):
        cat = self.tkvar.get()
        if cat in itemTypes:
            rows = dao.viewType(cat)
        else:
            rows = dao.viewCategory(cat)

        self.updateDisplay(rows)

    def viewCorresp(self):
        try:
            dict = self.getSelectedValues()
            if dict["type"] == 'gun':
                rows = dao.getWeaponAndCorresponding(self.name_text.get())
            else:
                rows = dao.getWeaponsFromAccessoire(self.name_text.get())

            self.updateDisplay(rows)
        except IndexError:
            pass

    def searchByName(self):
        rows = dao.searchByName(self.name_text.get())
        self.updateDisplay(rows)

    def updateSel(self):
        rows = dao.update(self.getEditedValues())
        self.updateDisplay(rows)
        self.updateNomVars()

    def updateXML(self):
        XMLtypes.update(xmlParsing4.types, xmlParsing4.tree, xmlParsing4.myXML)

    def clearTree(self):
        if self.tree.get_children() != ():
            self.tree.delete(*self.tree.get_children())

    def fillEntryBoxes(self, event):
        try:
            dict = self.getSelectedValues()
            self.nameEntry.delete(0, END)
            self.nameEntry.insert(END, dict["name"])

            self.nominalEntry.delete(0, END)
            self.nominalEntry.insert(END, dict["nominal"])

            self.minEntry.delete(0, END)
            self.minEntry.insert(END, dict["min"])

            self.restockEntry.delete(0, END)
            self.restockEntry.insert(END, dict["restock"])

            self.lifetimeEntry.delete(0, END)
            self.lifetimeEntry.insert(END, dict["lifetime"])

        except IndexError:
            pass

    def getSelectedValues(self):
        val = {}
        dict = self.tree.item(self.tree.focus())
        val["name"] = dict["text"]
        val["nominal"] = dict["values"][0]
        val["min"] = dict["values"][1]
        val["restock"] = dict["values"][2]
        val["lifetime"] = dict["values"][3]
        val["type"] = dict["values"][4]

        return val

    def getEditedValues(self):
        val = {"name": self.name_text.get(), "nominal": self.nominal_text.get(), "min": self.min_text.get(),
               "restock": self.restock_text.get(), "lifetime": self.lifetime_text.get()}
        return val

    def updateDisplay(self, rows):
        self.clearTree()
        for row in rows:
            self.tree.insert('', "end", text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))


window = Tk()
Window(window)

window.mainloop()
