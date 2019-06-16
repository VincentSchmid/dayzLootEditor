from tkinter import messagebox
import tkinter.filedialog as filediag
import time
import tkinter.filedialog as filediag
from os import getcwd
from os import remove
from os.path import abspath
from os.path import join
from tkinter import messagebox

try:
    from application import dao, xmlParser
except ModuleNotFoundError:
    import dao
    import xmlParser


def deleteParams():
    remove(abspath(join(getcwd(), "..", "data", "config.txt")))


def openFile(fileEnding):
    return filediag.askopenfilename(filetypes=[(fileEnding.upper() + " File", "*." + fileEnding)])


def saveAsFile(fileEnding, read):
    try:
        return filediag.asksaveasfile(mode=read, defaultextension=fileEnding)
    except TypeError:
        pass


def saveDB():
    fname = saveAsFile("sql", "w+")
    if fname != None:
        dao.backupDatabase(fname)


def writeFile(output, location):
    f = open(location, "wb+")
    f.write(output)
    f.close()


def showError(parent, title, message):
    messagebox.showinfo(parent=parent, title=title, message=message)


def askUser(title, question):
    MsgBox = messagebox.askquestion(title, question, icon='warning')
    return MsgBox == "yes"


def connectionSuccess(root):
    showError(root, "Success", "Connection Successfull!")


def askOverwrite():
    return askUser("Overwrite", "Are you sure you want to overwrite existing Database?")


def writeConfig(user, pwd, port, database, server):
    with open(abspath(join(getcwd(), "..", "data", "config.txt")), 'w+') as the_file:
        the_file.write(user + '\n')
        the_file.write(pwd + '\n')
        the_file.write(port + '\n')
        the_file.write(database + '\n')
        the_file.write(server + '\n')


def readConfig():
    try:
        with open(abspath(join(getcwd(), "..", "data", "config.txt")), 'r') as the_file:
            content = the_file.readlines()
            content = [x.strip() for x in content]
            return content
    except FileNotFoundError:
        dao.setConnectionParams("root", "rootroot", "3306", "dayzitems", "127.0.0.1")


def loadTypesXML(dir):
    items = xmlParser.parseAll(dir)
    params = xmlParser.createStringFromKeys(items[0])
    itemVal = xmlParser.createValues(items)
    time.sleep(1)
    dao.insertItems(params, itemVal)
    time.sleep(1)
    matches = xmlParser.gunsAndMatchingItem(items)
    dao.createCombos(matches)


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
