import tkinter.filedialog as filediag
from os import getcwd
from os import remove
from os.path import abspath
from os.path import join
from time import sleep
from tkinter import messagebox

try:
    from application import dao, xmlParser
except ModuleNotFoundError:
    import dao
    import xmlParser

dataPath = abspath(join(getcwd(), "..", "data"))

def deleteParams():
    remove(dataPath + "\\config.txt")


def openFile(fileEnding):
    return filediag.askopenfilename(filetypes=[(fileEnding.upper() + " File", "*." + fileEnding)])


def saveAsFile(fileEnding, read):
    try:
        return filediag.asksaveasfile(mode=read, defaultextension=fileEnding)
    except TypeError:
        pass


def saveDB():
    fname = saveAsFile("sql", "wb+")
    if fname != None:
        dao.backupDatabase(fname)


def copyFile(fromdir, todir):
    with open(fromdir) as f:
        with open(todir, "w+") as f1:
                    f1.write(f.read())


def showError(parent, title, message):
    messagebox.showinfo(parent=parent, title=title, message=message)


def askUser(title, question):
    MsgBox = messagebox.askquestion(title, question, icon='warning')
    return MsgBox == "yes"


def connectionSuccess(root):
    showError(root, "Success", "connection successful!")


def askOverwrite():
    return askUser("Overwrite", "Are you sure you want to overwrite existing database?")


def writeConfig(user, pwd, port, database, server):
    with open(dataPath + "\\config.txt", 'w+') as the_file:
        the_file.write(user + '\n')
        the_file.write(pwd + '\n')
        the_file.write(port + '\n')
        the_file.write(database + '\n')
        the_file.write(server + '\n')


def readConfig():
    try:
        with open(dataPath + "\\config.txt", 'r') as the_file:
            content = the_file.readlines()
            content = [x.strip() for x in content]
            return content
    except FileNotFoundError:
        dao.setConnectionParams("root", "rootroot", "3306", "dayzitems", "127.0.0.1")


def writeTypesToDatabase(dir):
    items = xmlParser.parseXML(dir)
    params = xmlParser.createStringFromKeys(items[0])
    itemVal = xmlParser.createValues(items)
    matches = xmlParser.gunsAndMatchingItem(items)

    sleep(1)
    dao.insertItems(params, itemVal)
    sleep(1)
    dao.createCombos(matches)


def appendTypesToDatabase(xml, root):
    count = 0
    duplicates = []
    message = " Items where added to database, duplicate items where not added:\n"
    items = xmlParser.parseXML(xml)
    params = xmlParser.createStringFromKeys(items[0])
    itemVal = xmlParser.createValues(items)
    matches = xmlParser.gunsAndMatchingItem(items)

    for item in itemVal:
        err = dao.insertItem(params, item)

        if err == 1:
            message += item[0] + "\n"

        else:
            count += 1

    showError(root, "Success", str(count) + message)


def saveSourceTypes(dir, dbName):
    copyFile(dir, dataPath + "\\SOURCETYPES_"+dbName+".xml")



def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
