from os import getcwd
from os import path
from os.path import abspath
from os.path import join
from subprocess import Popen, PIPE
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

try:
    from application import xmlParsing4, writeItemToXML, dao, distibutor
except ModuleNotFoundError:
    import xmlParsing4
    import writeItemToXML
    import dao
    import distibutor

class ConnectionWindow(object):
    def __init__(self, root):
        self.window = Toplevel(root)
        MODES = [("New Database", "1"), ("Use Existing", "0")]
        v = StringVar()
        v.set("0")


        self.entryFrame = Frame(self.window)
        self.entryFrame.grid(row=1, column=0, sticky="n,w,e", padx=30)

        #Host
        Label(self.entryFrame, text="Host:").grid(row=1, column=0, sticky="w")

        self.HostName = StringVar()
        self.HostName.set("localhost")
        self.nameEntry = Entry(self.entryFrame, textvariable=self.HostName)
        self.nameEntry.grid(row=1, column=1, sticky="e", pady=5)

        #Port
        Label(self.entryFrame, text="Port:").grid(row=2, column=0, sticky="w")

        self.port = StringVar()
        self.port.set("3306")
        self.nameEntry = Entry(self.entryFrame, textvariable=self.port)
        self.nameEntry.grid(row=2, column=1, sticky="e", pady=5)

        #Username
        Label(self.entryFrame, text="Username:").grid(row=4, column=0, sticky="w")

        self.username = StringVar()
        self.username.set("root")
        self.DBEntry = Entry(self.entryFrame, textvariable=self.username)
        self.DBEntry.grid(row=4, column=1, sticky="e", pady=5)

        #Password
        Label(self.entryFrame, text="Password:").grid(row=5, column=0, sticky="w")

        self.password = StringVar()
        self.password.set("rootroot")
        self.DBEntry = Entry(self.entryFrame, textvariable=self.password)
        self.DBEntry.grid(row=5, column=1, sticky="e", pady=5)

        #Database
        Radiobutton(self.entryFrame, text=MODES[0][0], variable=v, value=MODES[0][1]).grid(row=6, column=0, pady=10)
        Radiobutton(self.entryFrame, text=MODES[1][0], variable=v, value=MODES[1][1]).grid(row=6, column=1)

        Label(self.entryFrame, text="Database:").grid(row=7, column=0, sticky="w")

        self.database = StringVar()
        self.database.set("dayzitems")
        self.DBEntry = Entry(self.entryFrame, textvariable=self.database)
        self.DBEntry.grid(row=7, column=1, sticky="e", pady=5)

        buttonFrame = Frame(self.window)
        buttonFrame.grid(row=2, column=0, columnspan=3, pady=10)

        Button(buttonFrame, text="Create / Test", width=12,).grid(row=0, column=1, sticky="w", padx=5)
        Button(buttonFrame, text="Set", width=12,).grid(row=0, column=3, sticky="e", padx=5)


window = Tk()
ConnectionWindow(window)

window.mainloop()
