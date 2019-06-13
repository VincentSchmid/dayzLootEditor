import tkinter.filedialog as filediag

def openFile(fileEnding):
    return filediag.askopenfilename(filetypes=[(fileEnding.upper() + " File", "*."+fileEnding)])

def writeFile(output, location):
    f = open(location, "wb+")
    f.write(output)
    f.close()