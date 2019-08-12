import tkinter.filedialog as filediag
from os import getcwd
from os import remove
from os.path import abspath
from os.path import join
from time import sleep
from tkinter import END
from tkinter import messagebox

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
    if fname is not None:
        dao.backupDatabase(fname)


def copyFile(fromdir, todir):
    with open(fromdir) as f:
        with todir as f1:
            f1.write(f.read())


def showError(parent, title, message):
    messagebox.showinfo(parent=parent, title=title, message=message)


def showUpgradeError(parent):
    showError(parent, "Upgrade Your Database", "Your Database is not compatible with this version "
                                               "of the software.\n"
                                               "After Launch go to Database > Detect Subtypes")


def askUser(title, question):
    MsgBox = messagebox.askquestion(title, question, icon='warning')
    return MsgBox == "yes"


def connectionSuccess(root):
    showError(root, "Success", "connection successful!")


def askOverwrite():
    return askUser("Overwrite", "Are you sure you want to overwrite existing database?")


def writeConfig(user, pwd, port, database, server, odbcv):
    with open(dataPath + "\\config.txt", 'w+') as the_file:
        the_file.write(user + '\n')
        the_file.write(pwd + '\n')
        the_file.write(port + '\n')
        the_file.write(database + '\n')
        the_file.write(server + '\n')
        the_file.write(odbcv + '\n')


def readConfig():
    try:
        with open(dataPath + "\\config.txt", 'r') as the_file:
            content = the_file.readlines()
            content = [x.strip() for x in content]
            return content
    except FileNotFoundError:
        dao.setConnectionParams("root", "rootroot", "3306", "dayzitems", "127.0.0.1", "8.0")


def writeTypesToDatabase(dir):
    items = xmlParser.parseFromFile(dir)
    params = xmlParser.createStringFromKeys(items[0])
    itemVal = xmlParser.createValues(items)
    sleep(1)
    dao.insertItems(params, itemVal)
    sleep(1)
    matches = xmlParser.gunsAndMatchingItem(items)
    try:
        dao.createCombos(matches)
    except Exception:
        print("An exception occured when trying to create item Links")


def getItemsFromTraderFile(dir, root):
    items = []
    category = ""
    count = 0
    with open(dir) as the_file:

        for line in the_file:
            # remove all comments
            line = line.partition('//')[0]
            line = line.rstrip()

            #set category
            if "<Category>" in line:
                category = line.partition(">")[2].strip()

            if category != "" and "," in line:
                try:
                    values = line.split(",")
                    name = values[0].strip()
                    traderCat = values[1].strip()
                    buyPrice = values[2].strip()
                    sellPrice = values[3].strip()

                    items.append([buyPrice, sellPrice, traderCat, category, name])
                    count += 1
                except IndexError:
                    showError(root, "Error in File",
                              "There might be an error in this line:\n" + " ".join(line.split()))

    return items, count


def writeToDBFromTrader(dir, root=None):
    result = getItemsFromTraderFile(dir, root)
    dao.setTraderValues(result[0])
    showError(root, "Trader File Loaded", "Trader file was loaded successfully\n" + str(result[1]) + " Items have been changed")


def appendTypesToDatabase(xml, root, mod, useNew):
    count = 0
    successes = []
    message = " Items where added to database, duplicate items where not added:\n"
    items = xmlParser.parseFromString(xml, mod)
    params = xmlParser.createStringFromKeys(items[0])
    itemVal = xmlParser.createValues(items)
    matches = xmlParser.gunsAndMatchingItem(items)

    if len(itemVal) > 100:
        sleep(1)

    for item in itemVal:
        err = dao.insertItem(params, item)
        if err == 1:
            message += item[0] + "\n"
            if useNew:
                itemDict = dao.getDict(item)
                itemDict["rarity"] = dao.getRarity(item[0])
                itemDict["mod"] = mod
                itemDict["usage"] = item[11:24]
                itemDict["tier"] = item[24:28]
                dao.update(itemDict)
        else:
            count += 1
            successes.append(item[0])

    if len(itemVal) > 100:
        sleep(1)

    if len(matches) != 0:
        dao.createCombos(matches)

    showError(root, "Success", str(count) + message)
    return successes


def removeLastLineFromFile(path):
    readFile = open(path)
    lines = readFile.readlines()
    readFile.close()
    w = open(path, 'w')
    lines[-2] = lines[-2].strip("\t").strip("\n")
    w.writelines([item for item in lines[:-1]])
    w.writelines("  ")


def selectItemsFromLB(listBox, rows):
    for i in range(len(rows)):
        if rows[i] == 1:
            listBox.select_set(i)


def updateListBox(box, rows):
    box.delete(0, END)
    for row in rows:
        box.insert(END, row)


def getMods():
    return dao.getMods()


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


def addToClipboard(root, string):
    root.clipboard_clear()
    root.clipboard_append(string)
    root.update()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False