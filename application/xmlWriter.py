import dao
import items
import windows
import xmlParser
import categories as cats


def orderModList(mods):
    for i in range(len(mods)):
        if mods[i] == "Vanilla":
            tmp = mods[0]
            mods[0] = "Vanilla"
            mods[i] = tmp

    return mods


def getXmlBlock(row, namalsk):
    item = items.Item()
    item.fillFromVal(row)
    return item.getXML(namalsk)


def update(dir, includedMods, namalsk=False):
    #fix this so it does not need written anymore

    mod_index = len(cats.loot_economy) + len(cats.usages) + len(cats.tiers) + len(cats.tags) + len(cats.flags) + 2

    written = []
    includedMods = orderModList(includedMods)
    f = dir
    items = dao.getAllItems()
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n")
    f.write("<types>\n")
    for mod in includedMods:
        f.write("  <!--{}--> \n".format(mod))
        for item in items:
            if item[mod_index] in mod and item[0] not in written:
                f.write(getXmlBlock(item, namalsk))
                written.append(item[0])
    f.write("</types>\n")


def exportSpawnable():
    fname = windows.saveAsFile("xml", "w+")
    if fname is not None:
        spawnable = ""
        rifles = xmlParser.itemFromRows(dao.getType("rifles"))
        pistols = xmlParser.itemFromRows(dao.getType("pistols"))
        gun = xmlParser.itemFromRows(dao.getType("gun"))

        items = gun + rifles + pistols
        for item in items:
            if item.mod != "Vanilla":
                if item.nominal != 0:
                    spawnable += item.getSpawnableTypes()

        fname.write(spawnable)


def is_craftable(item):
    return item[-5] == 1


def does_spawn(item):
    return item[5] != 0
