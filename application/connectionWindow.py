from tkinter import *

try:
    from application import xmlParser, xmlWriter, dao, distibutor, windows
except ModuleNotFoundError:
    import xmlParser
    import xmlWriter
    import dao
    import distibutor
    import windows


class ConnectionWindow(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        self.window.grab_set()

        self.user = "root"
        self.pwd = "rootroot"
        self.prt = "3306"
        self.dbName = "dayzitems"
        self.server = "localhost"

        try:
            c = windows.readConfig()
            self.user = c[0]
            self.pwd = c[1]
            self.prt = c[2]
            self.dbName = c[3]
            self.server = c[4]

        except FileNotFoundError:
            pass

        self.entryFrame = Frame(self.window)
        self.entryFrame.grid(row=1, column=0, sticky="n,w,e", padx=30)

        # Host
        Label(self.entryFrame, text="Host:").grid(row=1, column=0, sticky="w")

        self.HostName = StringVar()
        self.HostName.set(self.server)
        self.nameEntry = Entry(self.entryFrame, textvariable=self.HostName)
        self.nameEntry.grid(row=1, column=1, sticky="e", pady=5)

        # Port
        Label(self.entryFrame, text="Port:").grid(row=2, column=0, sticky="w")

        self.port = StringVar()
        self.port.set(self.prt)
        self.nameEntry = Entry(self.entryFrame, textvariable=self.port)
        self.nameEntry.grid(row=2, column=1, sticky="e", pady=5)

        # Username
        Label(self.entryFrame, text="Username:").grid(row=4, column=0, sticky="w")

        self.username = StringVar()
        self.username.set(self.user)
        self.DBEntry = Entry(self.entryFrame, textvariable=self.username)
        self.DBEntry.grid(row=4, column=1, sticky="e", pady=5)

        # Password
        Label(self.entryFrame, text="Password:").grid(row=5, column=0, sticky="w")

        self.password = StringVar()
        self.password.set(self.pwd)
        self.DBEntry = Entry(self.entryFrame, textvariable=self.password)
        self.DBEntry.grid(row=5, column=1, sticky="e", pady=5)

        # Database

        MODES = [("New Database", "create"), ("Use Existing", "use")]
        self.v = StringVar()
        self.v.set("use")

        Radiobutton(self.entryFrame, text=MODES[0][0], variable=self.v, value=MODES[0][1]).grid(row=6, column=0,
                                                                                                pady=10)
        Radiobutton(self.entryFrame, text=MODES[1][0], variable=self.v, value=MODES[1][1]).grid(row=6, column=1)

        Label(self.entryFrame, text="Database:").grid(row=7, column=0, sticky="w")

        self.database = StringVar()
        self.database.set(self.dbName)
        self.DBEntry = Entry(self.entryFrame, textvariable=self.database)
        self.DBEntry.grid(row=7, column=1, sticky="e", pady=5)

        # Types
        Label(self.entryFrame, text="Types.xml:").grid(row=8, column=0, sticky="w")

        self.typesDir = StringVar()
        self.DBEntry = Entry(self.entryFrame, textvariable=self.typesDir)
        self.DBEntry.grid(row=8, column=1, sticky="e", pady=5)

        Button(self.entryFrame, text="...", height=1, command=self.openTypes).grid(row=8, column=2, sticky="w")

        buttonFrame = Frame(self.window)
        buttonFrame.grid(row=2, column=0, columnspan=3, pady=10)

        Button(buttonFrame, text="Create / Test", width=12, command=self.createTest).grid(row=0, column=1, sticky="w",
                                                                                          padx=5)
        Button(buttonFrame, text="Set", width=12, command=self.set).grid(row=0, column=3, sticky="e", padx=5)

        windows.center(self.window)
        self.window.wait_window()

    def openTypes(self):
        self.typesDir.set(windows.openFile("xml"))

    def createTest(self):
        if self.v.get() == "create":
            self.createDatabase()
            windows.connectionSuccess(self.window)
            if self.typesDir.get() != "":
                windows.writeTypesToDatabase(self.typesDir.get())
        else:
            self.testDB()

    def createDatabase(self):
        self.passParams()
        try:
            dao.createDB(self.database.get())
            dao.loadDB(windows.dataPath + "\\GENESIS.sql")
        except Exception as e:
            windows.showError(self.window, "Error", "Failed to connect:\n" + str(e))
            windows.deleteParams()

    def testDB(self):
        self.passParams()
        try:
            dao.getNominalByType("gun")
            windows.connectionSuccess(self.window)
        except Exception as e:
            windows.showError(self.window, "Error", "Failed to connect:\n" + str(e))
            windows.deleteParams()

    def set(self):
        self.passParams()
        self.window.destroy()

    def passParams(self):
        dao.setConnectionParams(self.username.get(),
                                self.password.get(),
                                self.port.get(),
                                self.database.get(),
                                self.HostName.get(),
                                "5.3")


def testWindow():
    window = Tk()
    ConnectionWindow(window)

    window.mainloop()
