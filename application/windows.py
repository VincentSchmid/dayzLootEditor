from tkinter import messagebox
import tkinter.filedialog as filediag
from os import path
from os.path import abspath
from os.path import join
from os import getcwd


def openFile(fileEnding):
    return filediag.askopenfilename(filetypes=[(fileEnding.upper() + " File", "*."+fileEnding)])


def writeFile(output, location):
    f = open(location, "wb+")
    f.write(output)
    f.close()


def showError(title, message):
    messagebox.showinfo(title, message)


def writeConfig(user, pwd, port, database, server):
    with open(abspath(join(getcwd(), "..", "data", "config.txt")), 'w+') as the_file:
        the_file.write(user+'\n')
        the_file.write(pwd+'\n')
        the_file.write(port+'\n')
        the_file.write(database+'\n')
        the_file.write(server+'\n')


def readConfig():
    with open(abspath(join(getcwd(), "..", "data", "config.txt")), 'r') as the_file:
        content = the_file.readlines()
        content = [x.strip() for x in content]
        return content