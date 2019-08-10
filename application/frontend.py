from time import sleep
from tkinter import *
from tkinter import ttk

import addItems
import categories
import connectionWindow
import dao
import distibutor
import itemLinker
import upgradeDB
import windows
import xmlParser
import xmlWriter
from assignSubTypes import TraderEditor
from autocompleteCombobox import Combobox_Autocomplete

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
        self.window.wm_title("Loot Editor v0.91")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.changed = False
        self.availableMods = windows.getMods()
        self.selectedMods = self.availableMods
        self.activatedFields = set()
        self.sorted = ""
        self.reverse = False

        self.createMenuBar()
        self.createEntryBar()
        self.createTreeview()
        self.createSideBar()
        self.createDistibutionBlock()
        self.createMultiplierBlock()
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
        self.viewCategroy()

    def createMenuBar(self):
        menubar = Menu(self.window)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load types.xml...", command=self.loadTypesXML)
        filemenu.add_command(label="Load Database...", command=self.loadDB)
        filemenu.add_separator()
        filemenu.add_command(label="Export types.xml...", command=self.saveXML)
        filemenu.add_command(label="Save Database As...", command=self.saveDB)
        filemenu.add_command(label="(Beta) Export Spawnabletypes...", command=self.exportSpawnable)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        databasemenu = Menu(menubar, tearoff=0)
        databasemenu.add_command(label="Connect...", command=self.openConnectionWindow)
        databasemenu.add_command(label="Detect Subtypes", command=self.upgradeDB)
        databasemenu.add_separator()
        databasemenu.add_command(label="Add items...", command=self.openAddItems)
        databasemenu.add_command(label="Create item links...", command=self.openitemLinker)
        databasemenu.add_command(label="Trader Editor...", command=self.openTraderEditor)
        menubar.add_cascade(label="Database", menu=databasemenu)

        self.modsmenu = Menu(menubar, tearoff=0)
        self.modSelectionVars = []

        for mod in self.availableMods:
            intVar = IntVar()
            intVar.set(1)
            intVar.trace("w", self.updateModSelection)
            self.modSelectionVars.append(intVar)
            self.modsmenu.add_checkbutton(label=mod, variable=intVar)

        menubar.add_cascade(label="Mods In Use", menu=self.modsmenu)

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
        Label(self.EFValues, text="Usages").grid(row=5, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="Tiers").grid(row=6, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="Type").grid(row=7, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="Subtype").grid(row=8, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="rarity").grid(row=9, column=0, sticky="w", pady=5)
        Label(self.EFValues, text="mod").grid(row=10, column=0, sticky="w", pady=5)

        self.name_text = StringVar()
        self.nameEntry = Entry(self.EFValues, textvariable=self.name_text)
        self.nameEntry.grid(row=0, column=1, sticky="w")

        self.nominal_text = StringVar()
        self.nominalEntry = Entry(self.EFValues, textvariable=self.nominal_text, width=8)
        self.nominalEntry.grid(row=1, column=1, sticky="w")
        self.nominalEntry.bind("<FocusIn>", self.addEditedVal)
        self.nominalEntry.val = self.nominal_text

        self.min_text = StringVar()
        self.minEntry = Entry(self.EFValues, textvariable=self.min_text, width=8)
        self.minEntry.grid(row=2, column=1, sticky="w")
        self.minEntry.bind("<FocusIn>", self.addEditedVal)
        self.minEntry.val = self.min_text

        self.restock_text = StringVar()
        self.restockEntry = Entry(self.EFValues, textvariable=self.restock_text, width=8)
        self.restockEntry.grid(row=3, column=1, sticky="w")
        self.restockEntry.bind("<FocusIn>", self.addEditedVal)
        self.restockEntry.val = self.min_text

        self.lifetime_text = StringVar()
        self.lifetimeEntry = Entry(self.EFValues, textvariable=self.lifetime_text, width=8)
        self.lifetimeEntry.grid(row=4, column=1, sticky="w")
        self.lifetimeEntry.bind("<FocusIn>", self.addEditedVal)
        self.lifetimeEntry.val = self.lifetime_text

        self.usageListBox = Listbox(self.EFValues, height=len(categories.usages), selectmode='multiple',
                                    exportselection=False)
        self.usageListBox.grid(row=5, column=1, pady=5, sticky="w")
        self.usageListBox.bind("<FocusIn>", self.addEditedVal)

        self.tierListBox = Listbox(self.EFValues, height=4, selectmode='multiple', exportselection=False)
        self.tierListBox.grid(row=6, column=1, pady=5, sticky="w")
        self.tierListBox.bind("<FocusIn>", self.addEditedVal)

        windows.updateListBox(self.usageListBox, categories.usages)
        windows.updateListBox(self.tierListBox, categories.tiers)

        self.typeEntrySel = StringVar()
        self.typeEntrySel.set('')
        self.typeEntrySel.trace("w", self.typeSelChange)
        self.typeOption = OptionMenu(self.EFValues, self.typeEntrySel, *xmlParser.selection[:-1])
        self.typeOption.grid(row=7, column=1, sticky="w", pady=5)

        self.subtypeAutoComp = Combobox_Autocomplete(self.EFValues, dao.getSubtypes(), highlightthickness=1)
        self.subtypeAutoComp.grid(row=8, column=1, sticky="w", pady=5)
        self.subtypeAutoComp.bind("<FocusIn>", self.addEditedVal)

        self.raritySel = StringVar()
        self.raritySel.set('undefined')
        self.rarityTrace = self.raritySel.trace("w", self.raritySelChange)

        self.rarityOption = OptionMenu(self.EFValues, self.raritySel, *rarities9.values())
        self.rarityOption.grid(row=9, column=1, sticky="w", pady=5)

        self.mod_text = StringVar()
        self.modEntry = Entry(self.EFValues, textvariable=self.mod_text, width=14)
        self.modEntry.grid(row=10, column=1, sticky="w", pady=5)
        self.modEntry.bind("<ButtonRelease-1>", self.addEditedVal)
        self.modEntry.val = self.mod_text

        self.EFCheckboxe = Frame(self.entryFrame)
        self.EFCheckboxe.grid(row=1, column=0, columnspan=2, sticky="w")

        self.deLoot = IntVar()
        self.deLootOption = Checkbutton(self.EFCheckboxe, text='Dynamic Event', variable=self.deLoot)
        self.deLootOption.grid(row=0, column=0, sticky="w")
        self.deLootOption.bind("<Button-1>", lambda e: self.addEditedVal(self.deLootOption.focus_set()))
        self.deLootOption.val = self.deLoot

        self.cargo = IntVar()
        self.cargoOption = Checkbutton(self.EFCheckboxe, text='Count in Cargo', variable=self.cargo)
        self.cargoOption.grid(row=1, column=0, sticky="w")
        self.cargoOption.bind("<Button-1>", lambda e: self.addEditedVal(self.cargoOption.focus_set()))
        self.cargoOption.val = self.cargo

        self.hoarder = IntVar()
        self.hoarderOption = Checkbutton(self.EFCheckboxe, text='Count in Hoarder', variable=self.hoarder)
        self.hoarderOption.grid(row=2, column=0, sticky="w")
        self.hoarderOption.bind("<Button-1>", lambda e: self.addEditedVal(self.hoarderOption.focus_set()))
        self.hoarderOption.val = self.hoarder

        self.map = IntVar()
        self.mapOption = Checkbutton(self.EFCheckboxe, text='Count in Map', variable=self.map)
        self.mapOption.grid(row=3, column=0, sticky="w")
        self.mapOption.bind("<Button-1>", lambda e: self.addEditedVal(self.mapOption.focus_set()))
        self.mapOption.val = self.map

        self.player = IntVar()
        self.playerOption = Checkbutton(self.EFCheckboxe, text='Count in Player', variable=self.player)
        self.playerOption.grid(row=4, column=0, sticky="w")
        self.playerOption.bind("<Button-1>", lambda e: self.addEditedVal(self.playerOption.focus_set()))
        self.playerOption.val = self.player

        Button(self.entryFrame, text="Update", width=12, command=self.updateSel) \
            .grid(row=3, column=0, pady=9)

        Button(self.entryFrame, text="Delete", width=12, command=self.deleteSel) \
            .grid(row=4, column=0, pady=5)

    def createTreeview(self):
        self.treeFrame = Frame(self.window)
        self.treeFrame.grid(row=0, column=1, sticky="nsew")

        self.treeFrame.grid_rowconfigure(0, weight=1)
        self.treeFrame.grid_columnconfigure(0, weight=1)

        columns = ('nominal', 'min', 'restock', 'lifetime', 'type', 'subtype', 'usage',
                   'tier', 'Dyn. Event', 'rarity', 'mod')

        self.tree = ttk.Treeview(self.treeFrame,
                                 columns=columns, height=40)
        self.tree.heading('#0', text='Name')
        self.tree.heading('#1', text='Nominal')
        self.tree.heading('#2', text='Min')
        self.tree.heading('#3', text='Restock')
        self.tree.heading('#4', text='Lifetime')
        self.tree.heading('#5', text='Type')
        self.tree.heading('#6', text='Subtype')
        self.tree.heading('#7', text='Usage')
        self.tree.heading('#8', text='Tier')
        self.tree.heading('#9', text='Dyn. Event')
        self.tree.heading('#10', text='Rarity')
        self.tree.heading('#11', text='Mod')
        self.tree.column('#0', stretch=NO)
        self.tree.column('#1', width=60, stretch=YES)
        self.tree.column('#2', width=60, minwidth=20, stretch=YES)
        self.tree.column('#3', width=80, stretch=YES)
        self.tree.column('#4', width=80, stretch=YES)
        self.tree.column('#5', width=60, stretch=YES)
        self.tree.column('#6', width=60, stretch=YES)
        self.tree.column('#7', width=270, stretch=NO)
        self.tree.column('#8', width=130, stretch=YES)
        self.tree.column('#9', width=80, stretch=YES)
        self.tree.column('#10', width=120, stretch=YES)
        self.tree.column('#11', width=120, stretch=YES)

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))

        self.tree.grid(row=0, column=0, sticky='nsew')
        self.treeview = self.tree

        vert = ttk.Scrollbar(self.treeFrame, orient=VERTICAL)
        hori = ttk.Scrollbar(self.treeFrame, orient=HORIZONTAL)

        vert.grid(row=0, column=1, sticky="ns")
        hori.grid(row=1, column=0, sticky="we")
        self.tree.config(yscrollcommand=vert.set)
        self.tree.config(xscrollcommand=hori.set)
        vert.config(command=self.tree.yview)
        hori.config(command=self.tree.xview)

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

        typeDrop = OptionMenu(self.distribution, self.distribSel, *xmlParser.selection) \
            .grid(row=0)

        Label(self.distribution, text="Target Nominal").grid(row=1, sticky=W)
        self.targetNominal = StringVar()
        self.targetNominal.set(str(dao.getNominalByType("gun")))
        self.desiredNomEntry = Entry(self.distribution, textvariable=self.targetNominal, width=14).grid(row=2, sticky=W)

        self.inclAmmo = IntVar()
        Checkbutton(self.distribution, text='Ammo', variable=self.inclAmmo).grid(row=3, sticky=W)
        self.inclMags = IntVar()
        Checkbutton(self.distribution, text='Mags', variable=self.inclMags).grid(row=4, sticky=W)

        self.targetAmmo = StringVar()
        self.targetAmmo.set(str(dao.getNominalByType("ammo")))
        self.targetAmmoEntry = Entry(self.distribution, textvariable=self.targetAmmo, width=5)
        self.targetAmmoEntry.grid(row=3, column=1, sticky=W)

        self.targetMag = StringVar()
        self.targetMag.set(str(dao.getNominalByType("mag")))
        self.targetMagEntry = Entry(self.distribution, textvariable=self.targetMag, width=5)
        self.targetMagEntry.grid(row=4, column=1, sticky=W)

        Button(self.distribution, text="Distribute", width=12, command=self.distribute).grid(row=7, columnspan=2,
                                                                                             pady=10)

    def createMultiplierBlock(self):
        self.multiplierFrame = LabelFrame(self.buttons, text="Loot Multiplier")
        self.multiplierFrame.grid(row=6, column=0, padx=20, pady=20)

        self.multiplier = StringVar()
        self.multiplier.set('0.00')

        ttk.Scale(self.multiplierFrame, from_=0, to_=5, length=150,
                  command=lambda s: self.multiplier.set('%0.2f' % float(s))).grid(column=0, row=2)

        ttk.Label(self.multiplierFrame, textvariable=self.multiplier).grid(column=0, row=1)

        Button(self.multiplierFrame, text="Update", command=self.multiplySel).grid(row=3)

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
            try:
                self.deltaNom[i].set(nominal - self.startNominals[i])
            except TypeError:
                self.deltaNom[i].set(nominal)

    def viewCategroy(self):
        cat = self.typeSel.get()
        if cat in categories.categories:
            rows = dao.getCategory(cat)
        elif cat in itemTypes:
            rows = dao.getType(cat)
        else:
            rows = dao.getAllItems()

        self.updateDisplay(rows)

    def viewLinked(self):
        try:
            type = self.getSelectedValues(self.tree.focus())["type"]
            rows = dao.getLinekd(self.name_text.get(), type)

            self.updateDisplay(rows)
        except IndexError:
            pass

    def addEditedVal(self, event):
        widget = self.window.focus_get()

        switcher = {
            self.nominalEntry: "nominal",
            self.minEntry: "min",
            self.restockEntry: "restock",
            self.lifetimeEntry: "lifetime",
            self.usageListBox: "usage",
            self.tierListBox: "tier",
            self.subtypeAutoComp: "subtype",
            self.modEntry: "mod",
            self.deLootOption: "deloot",
            self.cargoOption: "cargo",
            self.hoarderOption: "hoarder",
            self.mapOption: "map",
            self.playerOption: "player"
        }

        self.activatedFields.add(switcher.get(widget, "error"))

    def enterPress(self, event):
        if type(self.nameEntry.focus_get()) is type(self.nameEntry):
            if self.nameEntry.focus_get() is self.nameEntry:
                self.searchByName()
            else:
                self.updateSel()

    def searchByName(self):
        rows = dao.searchByName(self.name_text.get())
        self.updateDisplay(rows)

    def deleteSel(self):
        dao.deleteItem(self.getSelectedValues(self.tree.focus())["name"])

    def updateSel(self, multiplier=None):
        for element in self.tree.selection():
            val = self.getEditedValues(element)
            val["name"] = self.tree.item(element)["text"]
            if multiplier is not None:
                val["nominal"] = val["nominal"] * multiplier
                val["min"] = val["min"] * multiplier
            dao.update(val)
        rows = dao.reExecuteLastQuery()
        self.updateDisplay(rows)
        self.changed = True
        self.activatedFields.clear()
        self.refreshSubtypes()

    def refreshSubtypes(self):
        self.subtypeAutoComp.grid_forget()
        self.subtypeAutoComp = Combobox_Autocomplete(self.EFValues, dao.getSubtypes(), highlightthickness=1)
        self.subtypeAutoComp.grid(row=8, column=1, sticky="w", pady=5)
        self.subtypeAutoComp.bind("<FocusIn>", self.addEditedVal)

    def updateModMenu(self):
        newMods = self._checkForNewMod()
        for mod in newMods:
            if mod not in self.availableMods:
                self.addModMenu(mod)

    def addModMenu(self, mod):
        intVar = IntVar()
        intVar.set(1)
        intVar.trace("w", self.updateModSelection)
        self.modSelectionVars.append(intVar)
        self.modsmenu.add_checkbutton(label=mod, variable=intVar)
        self.availableMods.append(mod)
        self.selectedMods.append(mod)

    def clearModMenu(self):
        for mod in self.availableMods:
            self.modsmenu.delete(0)
        self.availableMods = []
        self.modSelectionVars = []

    def fillModMenu(self):
        databaseMods = windows.getMods()
        try:
            for mod in databaseMods:
                if mod not in self.availableMods:
                    self.addModMenu(mod)
        except AttributeError:
            pass

    def _checkForNewMod(self):
        newMods = []
        databaseMods = windows.getMods()
        for mod in databaseMods:
            if mod not in self.availableMods:
                newMods.append(mod)

        return newMods

    def updateModSelection(self, *args):
        self.selectedMods = []
        for i in range(len(self.availableMods)):
            if self.modSelectionVars[i].get() == 1:
                self.selectedMods.append(self.availableMods[i])

        self.updateDisplay(dao.reExecuteLastQuery())

    def distribute(self):
        self.backupDB("dayzitems_before_Distribute.sql")
        flags = [self.inclAmmo.get(), self.inclMags.get()]
        distibutor.distribute(self.distribSel.get(), int(self.targetNominal.get()), int(self.targetMag.get()),
                              int(self.targetAmmo.get()), flags)
        self.changed = True
        self.updateDisplay(dao.getType(self.distribSel.get()))

    def multiplySel(self):
        self.updateSel(float(self.multiplier.get()))

    # Save dialog, copies source types to new document, then edits the values
    def saveXML(self):
        xmlPath = windows.saveAsFile("xml", "w+")
        if xmlPath is not None:
            xmlWriter.update(xmlPath, self.selectedMods)

    def clearTree(self):
        if self.tree.get_children() != ():
            self.tree.delete(*self.tree.get_children())

    def fillEntryBoxes(self, event):
        try:
            dict = self.getSelectedValues(self.tree.focus())
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

            self.usageListBox.selection_clear(0, END)
            self.tierListBox.selection_clear(0, END)

            windows.selectItemsFromLB(self.usageListBox, dao.getUsages(dict["name"]))
            windows.selectItemsFromLB(self.tierListBox, dao.getTiers(dict["name"]))

            self.typeEntrySel.set(dict["type"])
            self.subtypeAutoComp.set_value(dict["subtype"])
            self.raritySel.set(dict["rarity"])
            self.mod_text.set(dict["mod"])

            self.deLoot.set(dict["deloot"])
            self.cargo.set(dict["cargo"])
            self.hoarder.set(dict["hoarder"])
            self.map.set(dict["map"])
            self.player.set(dict["player"])

            windows.addToClipboard(self.window, dict["name"])

            self.activatedFields.clear()
        except IndexError:
            pass

    def getSelectedValues(self, element):
        dict = self.tree.item(element)
        flags = dao.getFlags(dict["text"])

        val = {"name": dict["text"], "nominal": dict["values"][0], "min": dict["values"][1],
               "deloot": dict["values"][8], "restock": dict["values"][2], "lifetime": dict["values"][3],
               "type": dict["values"][4], "subtype": dict["values"][5], "rarity": dict["values"][9],
               "mod": dict["values"][10], "cargo": flags[0], "hoarder": flags[1], "map": flags[2], "player": flags[3],
               "flags": flags}

        return val

    def getEditedValues(self, element):
        selected = self.getSelectedValues(element)
        selected.pop("rarity")
        selected.pop("type")

        val = {"nominal": self.nominal_text.get(), "min": self.min_text.get(), "deloot": self.deLoot.get(),
               "restock": self.restock_text.get(), "lifetime": self.lifetime_text.get(), "mod": self.mod_text.get(),
               "usage": self.getEditedListBox(self.usageListBox, categories.usages),
               "tier": self.getEditedListBox(self.tierListBox, categories.tiers),
               "cargo": self.cargo.get(), "hoarder": self.hoarder.get(), "subtype": self.subtypeAutoComp.get(),
               "map": self.map.get(), "player": self.player.get()}

        for field in self.activatedFields:
            selected[field] = val[field]

        return selected

    def getEditedListBox(self, listBox, keys):
        selection = []
        for i in range(len(keys)):
            if i in listBox.curselection():
                selection.append(1)
            else:
                selection.append(0)

        return selection

    def getRaritySel(self):
        for k, v in rarities9.items():
            if self.raritySel.get() == v:
                return str(k)

    def updateDisplay(self, rows):
        displayedNom = 0
        self.clearTree()
        for row in rows:
            row = self.dictFromRow(row)
            if row["mod"] in self.selectedMods:
                displayedNom += row["nominal"]
                self.tree.insert('', "end", text=row["name"], values=(row["nominal"], row["min"], row["restock"],
                                                                      row["lifetime"], row["type"], row["subtype"],
                                                                      row["usage"], row["tier"], row["deloot"],
                                                                      row["rarity"], row["mod"]))
        self.updateNominalInfo()
        self.totalNomDisplayed.set(displayedNom)
        try:
            self.treeview_sort_column(self.tree, self.sorted, self.reverse)
        except Exception:
            pass
        self.updateDistribution()
        self.updateModMenu()

    def dictFromRow(self, row):
        return {"name": row[0], "nominal": row[5], "min": row[8], "restock": row[9], "lifetime": row[3],
                "type": row[2], "rarity": rarities9[row[36]], "deloot": row[34],
                "usage": self.createUsage(row[10:23]), "tier": self.createTier(row[23:27]), "mod": row[37],
                "usages": row[10:23], "tiers": row[23:27], "subtype": row[38], "buyprice": row[39],
                "sellprice": row[40], "tradercat": row[41], "traderExcl": row[42]}

    def createUsage(self, row):
        usageNames = categories.usages
        if sum(row) > 5:
            usageNames = categories.usagesAbr
        usage = ""

        if sum(row) == len(usageNames) - 1:
            usage = "everywhere except Coast"
        else:
            for i in range(len(categories.usages)):
                if row[i] == 1:
                    usage += usageNames[i] + " "
            if usage != "":
                usage = usage[:-1]

        return usage

    def createTier(self, row):
        tier = ""
        for i in range(len(categories.tiers)):
            if row[i] == 1:
                tier += categories.tiers[i] + ","
        if tier != "":
            tier = tier[:-1]
        return tier

    def updateDistribution(self):
        self.targetNominal.set(str(dao.getNominalByType("gun")))
        self.targetMag.set(str(dao.getNominalByType("mag")))

    def raritySelChange(self, *args):
        self.dropSelChange("rarity", self.raritySel.get())

    def typeSelChange(self, *args):
        self.dropSelChange("type", self.typeEntrySel.get())

    def valueChange(self, name, entryValue):
        return not self.getSelectedValues(self.tree.selection()[0])[name] == entryValue

    def dropSelChange(self, name, entryValue, *args):
        if self.valueChange(name, entryValue):
            for element in self.tree.selection():
                selVal = self.getSelectedValues(element)[name]
                rareEntry = self.raritySel.get()
                if selVal != rareEntry:
                    dao.updateDropValue(self.getSelectedValues(element)["name"], entryValue, name)

            self.updateDisplay(dao.reExecuteLastQuery())

    def distribSelChange(self, *args):
        for i in range(len(itemTypes)):
            if self.distribSel.get() == itemTypes[i]:
                self.targetNominal.set(self.nomVars[i].get())

    def on_close(self):
        if self.changed:
            self.backupDB("dayzitems.sql")
        self.window.destroy()

    def loadTypesXML(self):
        self.clearModMenu()
        fname = windows.openFile("xml")
        if fname != "":
            if windows.askOverwrite():
                windows.writeTypesToDatabase(fname)
        self.fillModMenu()

    def loadDB(self):
        self.clearModMenu()
        fname = windows.openFile("sql")
        if fname != "":
            dbName = dao.dropDB()
            dao.createDB(dbName)
            dao.loadDB(fname)
        try:
            self.fillModMenu()
        except Exception:
            sleep(0.4)

    def saveDB(self):
        windows.saveDB()

    def backupDB(self, filename):
        dao.backupDatabase(open(windows.dataPath + "\\" + filename, "wb+"))

    def exportSpawnable(self):
        xmlWriter.exportSpawnable()

    def openConnectionWindow(self):
        try:
            self.clearModMenu()
        except AttributeError:
            pass
        connectionWindow.ConnectionWindow(self.window)
        self.fillModMenu()

    def openAddItems(self):
        addItems.addItems(self.window)
        self.updateModMenu()

    def openitemLinker(self):
        itemLinker.itemLinker(self.window)

    def openTraderEditor(self):
        TraderEditor(self.window)

    def checkForDatabase(self):
        try:
            dao.getNominalByType("weapon")
            self.connectionOK = True
        except Exception:
            self.window.withdraw()
            self.openConnectionWindow()
            self.window.deiconify()

        try:
            dao.getSubtypes()
        except Exception:
            windows.showUpgradeError(self.window)
            if windows.askUser("Upgrade", "Do you want to upgrade your Database?"):
                self.upgradeDB()

    def upgradeDB(self):
        try:
            dao.addColumns()
        except Exception:
            pass
        if windows.askUser("Change Subtypes", "Software will set default subtypes.\n"
                                              "If you haven't set any subtypes yet it is save to click yes"):
            upgradeDB.findSubTypes(dao.getAllItems())

    def treeview_sort_column(self, tv, col, reverse):
        self.sorted = col
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)
        self.reverse = reverse

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))


window = Tk()
Window(window)
window.mainloop()
