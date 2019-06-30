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



def setType(xml, item):
    for col in xml:
        if col.tag == "lifetime":
            col.text = str(item.lifetime)

        if col.tag == "quantmin":
            col.text = str(item.quantmin)

        if col.tag == "quantmax":
            col.text = str(item.quantmax)

        if col.tag == "min":
            col.text = str(item.min)

        if col.tag == "nominal":
            col.text = str(item.nominal)

        if col.tag == "cost":
            col.text = str(item.cost)

        if col.tag == "restock":
            col.text = str(item.restock)

        if col.tag == "flags":
            for i in range(len(col.items())):
                col.set(xmlParser.flags[i], str(item.flags[i]))

# update(xmlParsing4.types, xmlParsing4.tree, xmlParsing4.myXML)
