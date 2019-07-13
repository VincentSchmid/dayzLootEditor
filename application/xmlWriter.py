
import xmlParser
import dao
import windows


def orderModList(mods):
    for i in range(len(mods)):
        if mods[i] == "Vanilla":
            tmp = mods[0]
            mods[0] = "Vanilla"
            mods[i] = tmp

    return mods


def getXmlBlock(row):
    item = xmlParser.Item()
    item.fillFromVal(row)
    return item.getXML()


def update(dir, includedMods):
    includedMods = orderModList(includedMods)
    f = dir
    items = dao.getAllItems()
    f.write("<types>\n")
    for mod in includedMods:
        f.write("  <!--{}--> \n".format(mod))
        for item in items:
            if item[5] != 0:
                if item[-1] in mod:
                    f.write(getXmlBlock(item))
    f.write("</types>\n")


def exportSpawnable():
    fname = windows.saveAsFile("xml", "w+")
    if fname is not None:
        spawnable = ""
        items = xmlParser.itemFromRows(dao.getType("gun"))
        for item in items:
            if item.mod != "Vanilla":
                if item.nominal != 0:
                    spawnable += item.getSpawnableTypes()

        fname.write(spawnable)
