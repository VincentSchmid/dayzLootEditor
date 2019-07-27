import xml.etree.ElementTree as ET

import items as itm
from categories import weaponSubTypes, categories
from items import removeModPrefixes

items = []

selection = weaponSubTypes + categories
selection.append("all items")


def parseFromString(xml, mod="Vanilla"):
    return _parseRoot(ET.fromstring(xml), mod)


def parseFromFile(dir):
    try:
        tree = ET.parse(dir)

    except ET.ParseError:
        raise Exception

    return _parseRoot(tree.getroot())


def _parseRoot(root, mod="Vanilla"):
    items = []
    itemValues = []

    for type in root:
        item = createItemFromTypeBlock(type, mod)
        items.append(item)

    return items


def createValues(items):
    values = []
    for i in items:
        values.append(createValuesFromItem(i))
    return values


def createItemFromTypeBlock(block, mod):
    item = itm.Item()
    item.fill(block, mod)
    return item


def createValuesFromItem(item):
    return list(item.parameters.values())


def createStringFromKeys(item):
    params = ""
    for k in item.parameters.keys():
        params += k + ", "
    params = params[:-2]
    return params


# returns a list of all items given that match with given name
def findMatchingItem(name, items):
    matches = []

    name = removeModPrefixes(name)

    if "_ak" in name.lower() or "akm" in name.lower():
        name = "ak_"
    if "mp5k" == name.lower():
        name = "mp5_"
    if "ump45" in name.lower():
        name = "ump_"
    if "saiga" in name.lower():
        name = "saiga"
    if "m4" in name.lower():
        name = "m4_"
    if "real" in name.lower():
        name = name[:-4]
    if "glock" in name.lower():
        name = "glock"
    if "ij70" in name.lower():
        name = "ij70"
    if "mosin" in name.lower():
        name = "mosin"
    if "vityaz" in name.lower():
        name = "vityaz"
    if name.lower().endswith("new"):
        name = name[:-3]
    if "colt" in name.lower():
        name = "colt"
    for i in items:
        if name in i.name and name != i.name:
            matches.append(i.name)
    return matches


def itemFromRows(rows):
    items = []
    for row in rows:
        item = itm.Item()
        item.fillFromVal(row)
        items.append(item)
    return items


# returns a list of tuples with each tuple containing (gun item.name, matching secondary item.name)
def gunsAndMatchingItem(items):
    matching = []
    for i in items:
        if i.type == "gun":
            matches = findMatchingItem(i.name, items)
            for m in matches:
                matching.append((i.name, m))
    return matching


# returns 1 if beginning wrong
# returns 2 if end wrong
# returns 0 if good
def checkIfTypesXML(text):
    if text.startswith("<type"):
        if text.endswith("</type>"):
            return 0
        else:
            return 2

    elif text.startswith("<types>"):
        if text.endswith("</types>"):
            return 0
        else:
            return 2
    else:
        return 1
