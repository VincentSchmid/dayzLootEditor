import xml.etree.ElementTree as ET

try:
    from application import xmlParser, dao, windows
except ModuleNotFoundError:
    import xmlParser
    import dao
    import windows


def createItem(row):
    item = xmlParser.Item()
    item.fillFromVal(row)
    return item.getXML()


def update(dir, includedMods):
    f = open(dir)
    items = dao.getAllItems()
    for item in items:
        if item[-1] in includedMods:
            f.write(createItem(item))
