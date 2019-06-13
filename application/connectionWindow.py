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

class ConnectToDB(object):
    def __init__(self, root):
        self.window = Toplevel(root)