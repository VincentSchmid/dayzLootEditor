from os import getcwd, path
import xml.etree.ElementTree as ET

try:
    from application import xmlParser, dao
except ModuleNotFoundError:
    import xmlParsing4
    import dao


def update(dir):
    tree = ET.parse(dir)
    types = tree.getroot()

    items = []
    for val in dao.getAllItems():
        val = val[:-1]
        item = xmlParser.Item()
        item.fillFromVal(val)
        items.append(item)

    for item in items:
        for xmlType in types:
            if item.name == xmlType.attrib["name"]:
                setType(xmlType, item)

    tree.write(dir)



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


#update(xmlParsing4.types, xmlParsing4.tree, xmlParsing4.myXML)