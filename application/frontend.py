from os import getcwd
from os import path
from tkinter import *
from tkinter import ttk

try:
    from application import xmlParser, writeItemToXML, dao, distibutor, connectionWindow, windows, addItems
except ModuleNotFoundError:
    import xmlParser
    import writeItemToXML
    import dao
    import distibutor
    import connectionWindow
    import windows
    import additems

itemTypes = ["gun", "ammo", "optic", "mag", "attachment"]

rarities9 = {0: "undefined",
             50: "Legendary",
             45: "Extremely Rare",
             40: "Very Rare",
             35: "Rare",
             30: "Somewhat Rare",
             25: "Uncommon",
             20: "Common",
             15: "Very Common",
             10: "All Over The Place"}

rarities5 = {15: "Common", 20: "Uncommon", 30: "Rare", 40: "Very Rare", 50: "Legendary", 0: "undefined"}


class Window(object):
    def __init__(self, window):
        self.window = window
        self.checkForDatabase()
        self.window.wm_title("Loot Editor v0.5")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.changed = False

        self.createMenuBar()
        self.createEntryBar()
        self.createTreeview()
        self.createSideBar()
        self.createDistibutionBlock()
        windows.center(self.window)

        # Keybindings
        self.tree.bind('<ButtonRelease-1>', self.fillEntryBoxes)
        self.window.bind('<Return>', self.enterPress)

        # make windows extendable
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.nomVars = []
        self.deltaNom = []
        self.startNominals = []
        self.totalNomDisplayed = StringVar()
        self.totalNomDisplayed.set(0)
        self.createNominalInfo()

    def createMenuBar(self):
        menubar = Menu(self.window)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load types.xml...", command=self.loadTypesXML)
        filemenu.add_command(label="Load Database...", command=self.loadDB)
        filemenu.add_separator()
        filemenu.add_command(label="Export types.xml...", command=self.saveXML)
        filemenu.add_command(label="Save Database As...", command=self.saveDB)
        filemenu.add_separator()
        filemenu.add_command(label="Add to database from types", command=self.openAddItems)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit")

        databasemenu = Menu(menubar, tearoff=0)
        databasemenu.add_command(label="Connect...", command=self.openConnectionWindow)
        menubar.add_cascade(label="Database", menu=databasemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="You're on your own...")
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.window.config(menu=menubar)

    def createEntryBar(self):
        self.entryFrame = Frame(self.window)
        self.entryFrame.grid(row=0, column=0, sticky="nw")

        self.EFValues = Frame(self.entryFrame)
        self.EFValues.grid(padx=8, pady=6)

        Label(self.EFValues, text="name").grid(row=0, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="nominal").grid(row=1, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="min").grid(row=2, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="restock").grid(row=3, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="lifetime").grid(row=4, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="rarity").grid(row=6, column=0, sticky="w", pady=5)

        self.name_text = StringVar()
        self.nameEntry = Entry(self.EFValues, textvariable=self.name_text)
        self.nameEntry.grid(row=0, column=1, sticky="w")

        self.nominal_text = StringVar()
        self.nominalEntry = Entry(self.EFValues, textvariable=self.nominal_text, width=8)
        self.nominalEntry.grid(row=1, column=1, sticky="w")

        self.min_text = StringVar()
        self.minEntry = Entry(self.EFValues, textvariable=self.min_text, width=8)
        self.minEntry.grid(row=2, column=1, sticky="w")

        self.restock_text = StringVar()
        self.restockEntry = Entry(self.EFValues, textvariable=self.restock_text, width=8)
        self.restockEntry.grid(row=3, column=1, sticky="w")

        self.lifetime_text = StringVar()
        self.lifetimeEntry = Entry(self.EFValues, textvariable=self.lifetime_text, width=8)
        self.lifetimeEntry.grid(row=4, column=1, sticky="w")

        self.raritySel = StringVar()
        self.raritySel.set('undefined')
        self.raritySel.trace("w", self.raritySelChange)

        OptionMenu(self.EFValues, self.raritySel, *rarities9.values()).grid(row=6, column=1, sticky="w")

        self.EFCheckboxe = Frame(self.entryFrame)
        self.EFCheckboxe.grid(row=1, column=0, columnspan=2, sticky="w")

        self.deLoot = IntVar()
        Checkbutton(self.EFCheckboxe, text='Dynamic Event', variable=self.deLoot).grid(row=0, column=0, sticky="w")

        Button(self.entryFrame, text="Update", width=12, command=self.updateSel) \
            .grid(row=3, column=0, pady=9)

    def createTreeview(self):
        self.treeFrame = Frame(self.window)
        self.treeFrame.grid(row=0, column=1, sticky="nsew")

        self.treeFrame.grid_rowconfigure(0, weight=1)
        self.treeFrame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.treeFrame,
                                 columns=('name', 'nominal', 'min', 'restock', 'lifetime', 'usage', 'tier', 'Dyn. Event', 'rarity'))
        self.tree.heading('#0', text='Name')
        self.tree.heading('#1', text='Nominal')
        self.tree.heading('#2', text='Min')
        self.tree.heading('#3', text='Restock')
        self.tree.heading('#4', text='Lifetime')
        self.tree.heading('#5', text='Type')
        self.tree.heading('#6', text='Usage')
        self.tree.heading('#7', text='Tier')
        self.tree.heading('#8', text='Dyn. Event')
        self.tree.heading('#9', text='Rarity')
        self.tree.column('#0', stretch=NO)
        self.tree.column('#1', width=60, stretch=YES)
        self.tree.column('#2', width=60, minwidth=20, stretch=YES)
        self.tree.column('#3', width=80, stretch=YES)
        self.tree.column('#4', width=80, stretch=YES)
        self.tree.column('#5', width=60, stretch=YES)
        self.tree.column('#6', width=270, stretch=NO)
        self.tree.column('#7', width=150, stretch=YES)
        self.tree.column('#8', width=80, stretch=YES)
        self.tree.column('#9', width=120, stretch=YES)

        self.tree.grid(row=0, column=0, sticky='nsew')
        self.treeview = self.tree

        sb1 = Scrollbar(self.treeFrame)
        sb1.grid(row=0, column=1, sticky="n,s")
        self.tree.config(yscrollcommand=sb1.set)
        sb1.config(command=self.tree.yview)

    def createSideBar(self):

        # todo get from backend
        self.choices = xmlParser.selection

        self.buttons = Frame(self.window)
        self.buttons.grid(row=0, column=2, sticky="n")

        self.typeSel = StringVar(window)
        self.typeSel.set('gun')

        OptionMenu(self.buttons, self.typeSel, *self.choices).grid(row=1, column=0)

        Button(self.buttons, text="Show items", width=12, command=self.viewCategroy).grid(row=2)
        Button(self.buttons, text="view linked items", width=12, command=self.viewLinked).grid(row=3)
        Button(self.buttons, text="search by name", width=12, command=self.searchByName).grid(row=4)

    def createDistibutionBlock(self):
        self.distribution = LabelFrame(self.buttons, text="Rarity Distribution")
        self.distribution.grid(row=5, column=0, padx=20, pady=20)

        self.distribSel = StringVar(window)
        self.distribSel.set('gun')
        self.distribSel.trace("w", self.distribSelChange)

        typeDrop = OptionMenu(self.distribution, self.distribSel, *xmlParser.selection)\
            .grid(row=0)

        Label(self.distribution, text="Target Nominal").grid(row=1, sticky=W)
        self.targetNominal = StringVar()
        self.targetNominal.set(str(dao.getNominalByType("gun")))
        self.desiredNomEntry = Entry(self.distribution, textvariable=self.targetNominal, width=14).grid(row=2, sticky=W)

        self.inclAmmo = IntVar()
        Checkbutton(self.distribution, text='Ammo', variable=self.inclAmmo).grid(row=3, sticky=W)
        self.inclMags = IntVar()
        Checkbutton(self.distribution, text='Mags', variable=self.inclMags).grid(row=4, sticky=W)

        self.targetMag = StringVar()
        self.targetMag.set(str(dao.getNominalByType("mag")))
        self.targetMagEntry = Entry(self.distribution, textvariable=self.targetMag, width=5)
        self.targetMagEntry.grid(row=4, column=1, sticky=W)

        Button(self.distribution, text="Distribute", width=12, command=self.distribute).grid(row=7, columnspan=2, pady=10)

    def createNominalInfo(self):
        self.infoFrame = Frame(self.window)
        self.infoFrame.grid(row=1, column=1, sticky="s,w,e")

        Label(self.infoFrame, text="overall nominal / delta:").grid(row=0, column=0)

        Label(self.infoFrame, text="Displayed:").grid(row=0, column=1)
        Label(self.infoFrame, textvariable=self.totalNomDisplayed).grid(row=0, column=2)
        i = 3

        for type in itemTypes:
            var = StringVar()
            deltaStart = StringVar()

            self.startNominals.append(dao.getNominalByType(type))
            var.set(dao.getNominalByType(type))
            self.nomVars.append(var)
            deltaStart.set(0)
            self.deltaNom.append(deltaStart)

            Label(self.infoFrame, text=type.capitalize() + ":").grid(row=0, column=i)
            Label(self.infoFrame, textvariable=var).grid(row=0, column=i + 1)
            Label(self.infoFrame, text="/").grid(row=0, column=i + 2)
            Label(self.infoFrame, textvariable=deltaStart).grid(row=0, column=i + 3)

            i += 4

    def updateNominalInfo(self):
        for i in range(len(self.nomVars)):
            nominal = dao.getNominalByType(itemTypes[i])
            self.nomVars[i].set(nominal)
            self.deltaNom[i].set(nominal - self.startNominals[i])

    def viewCategroy(self):
        cat = self.typeSel.get()
        if cat in xmlParser.categories:
            rows = dao.viewCategory(cat)
        elif cat in itemTypes:
            rows = dao.viewType(cat)
        else:
            rows = dao.getAllItems()

        self.updateDisplay(rows)

    def viewLinked(self):
        try:
            dict = self.getSelectedValues()
            if dict["type"] == 'gun':
                rows = dao.getWeaponAndCorresponding(self.name_text.get())
            else:
                rows = dao.getWeaponsFromAccessoire(self.name_text.get())

            self.updateDisplay(rows)
        except IndexError:
            pass

    def enterPress(self, event):
        if type(self.nameEntry.focus_get()) is type(self.nameEntry):
            if self.nameEntry.focus_get() is self.nameEntry:
                self.searchByName()
            else:
                self.updateSel()

    def searchByName(self):
        rows = dao.searchByName(self.name_text.get())
        self.updateDisplay(rows)

    def updateSel(self):
        for element in self.tree.selection():
            val = self.getEditedValues()
            val["name"] = self.tree.item(element)["text"]
            dao.update(val)
        rows = dao.reExecuteLastQuery()
        self.updateDisplay(rows)
        self.changed = True

    def distribute(self):
        self.backupDB("dayzitems_before_Distribute.sql")
        flags = [self.inclAmmo.get(), self.inclMags.get()]
        distibutor.distribute(self.distribSel.get(), int(self.targetNominal.get()), int(self.targetMag.get()), flags)
        self.changed = True
        self.updateDisplay(dao.viewType(self.distribSel.get()))

    def updateXML(self):
        xmlPath = windows.dataPath + "\\types.xml"
        writeItemToXML.update(xmlPath)

    def saveXML(self):
        xmlPath = windows.openFile("xml")
        if xmlPath != None:
            writeItemToXML.update(xmlPath)

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

            self.deLoot.set(dict["deloot"])

            self.raritySel.set(dict["rarity"])

        except IndexError:
            pass

    def getSelectedValues(self):
        dict = self.tree.item(self.tree.focus())
        val = {"name": dict["text"], "nominal": dict["values"][0], "min": dict["values"][1],
               "deloot": dict["values"][7],"restock": dict["values"][2], "lifetime": dict["values"][3],
               "type": dict["values"][4], "rarity": dict["values"][8]}

        return val

    def getEditedValues(self):
        val = {"nominal": self.nominal_text.get(), "min": self.min_text.get(), "deloot": self.deLoot.get(),
               "restock": self.restock_text.get(), "lifetime": self.lifetime_text.get(), "rarity": self.getRaritySel()}
        return val

    def getRaritySel(self):
        for k, v in rarities9.items():
            if self.raritySel.get() == v:
                return str(k)

    def updateDisplay(self, rows):
        self.clearTree()
        for row in rows:
            row = self.dictFromRow(row)
            self.tree.insert('', "end", text=row["name"], values=(row["nominal"], row["min"], row["restock"],
                                                                  row["lifetime"], row["type"],  row["usage"],
                                                                  row["tier"], row["deloot"], row["rarity"]))
        self.updateNominalInfo()
        self.totalNomDisplayed.set(sum(x[5] for x in rows))
        self.updateDistribution()

    def dictFromRow(self, row):
        return {"name": row[0], "nominal": row[5], "min": row[8], "restock": row[9], "lifetime": row[3],
                   "type": row[2], "rarity": rarities9[row[36]], "deloot": row[34],
                   "usage": self.createUsage(row[10:23]), "tier": self.createTier(row[23:27])}

    def createUsage(self, row):
        usageNames = xmlParser.usages
        if sum(row) > 5:
            usageNames = xmlParser.usagesAbr
        usage = ""

        if sum(row) == len(usageNames) - 1:
            usage = "everywhere except Coast"
        else:
            for i in range(len(xmlParser.usages)):
                if row[i] == 1:
                    usage += usageNames[i] + " "
            if usage != "":
                usage = usage[:-1]

        return usage

    def createTier(self, row):
        tier = ""
        for i in range(len(xmlParser.tiers)):
            if row[i] == 1:
                tier += xmlParser.tiers[i] + ","
        if tier != "":
            tier = tier[:-1]
        return tier

    def updateDistribution(self):
        self.targetNominal.set(str(dao.getNominalByType("gun")))
        self.targetMag.set(str(dao.getNominalByType("mag")))

    def raritySelChange(self, *args):
        if self.getSelectedValues()["rarity"] != self.raritySel.get():
            self.updateSel()

    def distribSelChange(self, *args):
        for i in range(len(itemTypes)):
            if self.distribSel.get() == itemTypes[i]:
                self.targetNominal.set(self.nomVars[i].get())

    def on_close(self):
        if self.changed:
            self.backupDB("dayzitems.sql")
        self.window.destroy()

    def loadTypesXML(self):
        fname = windows.openFile("xml")
        if fname != "":
            if windows.askOverwrite():
                windows.writeTypesToDatabase(fname)

    def loadDB(self):
        fname = windows.openFile("sql")
        if fname != "":
            dao.loadDB(fname)

    def saveDB(self):
        windows.saveDB()

    def backupDB(self, filename):
        dao.backupDatabase(open(windows.dataPath + "\\" + filename, "wb+"))

    def openConnectionWindow(self):
        connectionWindow.ConnectionWindow(self.window)

    def openAddItems(self):
        addItems.addItems(self.window)

    def checkForDatabase(self):
        try:
            dao.getNominalByType("weapon")
            self.connectionOK = True
        except Exception:
            self.window.withdraw()
            self.openConnectionWindow()
            self.window.deiconify()


window = Tk()
Window(window)
window.mainloop()
