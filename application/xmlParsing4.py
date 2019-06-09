from os import getcwd, path
import xml.etree.ElementTree as ET

use_big_XML = True
typesDir = path.abspath(path.join(getcwd(), "..", "data"))
docName = ["testTypes.xml", "types.xml"]

myXML = docName[1] if use_big_XML else docName[0]

myXML = path.join(typesDir, myXML)

tree = ET.parse(myXML)
types = tree.getroot()

items = []

itemTypes = ["gun", "ammo", "optic", "mag", "attachment"]

usages = ["Village",
          "Hunting",
          "Police",
          "Office",
          "Medic",
          "Coast",
          "Firefighter",
          "Town",
          "Industrial",
          "Military",
          "Prison",
          "School",
          "Farm"]

tiers = ["Tier1", "Tier2", "Tier3", "Tier4"]

tags = ["shelves", "floor"]

flags = ["count_in_cargo",
         "count_in_hoarder",
         "count_in_map",
         "count_in_player",
         "crafted",
         "deloot"]


def findMatchingItem(name, items):
    matches = []
    if "gp_" in name.lower():
        name = name[3:]
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


def findType(name, category):
    if category == "weapons":
        if isGun(name):
            return itemTypes[0]

        if isMag(name):
            return itemTypes[3]

        if isAmmo(name):
            return itemTypes[1]

        if isOptic(name):
            return itemTypes[2]

        return itemTypes[4]

    else:
        return category


def isGun(name):
    isGun = False

    if name.lower().startswith("gp_"):
        name = name[3:]

    if "camo" not in name and "black" not in name and "green" not in name and "sawed" not in name and "_" not in name \
            and "LRS" not in name and "Ammo" not in name and "Optic" not in name and "Suppressor" not in name \
            and "Goggles" not in name and "Light" not in name and "Mag":
        isGun = True

    return isGun;


def isAmmo(name):
    if "ammo" in name.lower():
        return True
    else:
        return False


def isOptic(name):
    name = name.lower()
    if "optic" in name or "lrs" in name:
        return True
    else:
        return False


def isMag(name):
    if "mag" in name.lower():
        return True
    else:
        return False


class Item():
    def __init__(self):
        self.name = ""
        self.category = ""
        self.lifetime = 0
        self.quantmin = -1
        self.quantmax = -1
        self.min = 0
        self.nominal = 0
        self.cost = 100
        self.restock = 0
        self.usages = set()
        self.tiers = set()
        self.tags = set()
        self.flags = []
        self.parameters = {}

    def fill(self, xml):
        xml.attrib["name"]
        for col in xml:
            if col.tag == "category":
                self.category = col.items()[0][1]

            if col.tag == "lifetime":
                self.lifetime = col.text

            if col.tag == "quantmin":
                self.quantmin = col.text

            if col.tag == "quantmax":
                self.quantmax = col.text

            if col.tag == "min":
                self.min = col.text

            if col.tag == "nominal":
                self.nominal = col.text

            if col.tag == "cost":
                self.cost = col.text

            if col.tag == "restock":
                self.restock = col.text

            if col.tag == "usage":
                self.usages.add(col.items()[0][1])

            if col.tag == "value":
                self.tiers.add(col.items()[0][1])

            if col.tag == "tag":
                self.tags.add(col.items()[0][1])

            if col.tag == "flags":
                for attr in col.items():
                    self.flags.append(attr[1])

        self.type = findType(self.name, self.category)
        self.createParams()

    def fillFromVal(self, val):
        self.name = val[0]
        self.category = val[1]
        self.lifetime = val[3]
        self.quantmin = val[4]
        self.nominal = val[5]
        self.cost = val[6]
        self.quantmax = val[7]
        self.min = val[8]
        self.restock = val[9]
        p = 10
        for i in range(len(usages)):
            if val[p] == 1:
                self.usages.add(usages[i])
            p += 1

        for i in range(len(tiers)):
            if val[p] == 1:
                self.tiers.add(tiers[i])
            p += 1

        for i in range(len(tags)):
            if val[p] == 1:
                self.tags.add(tags[i])
            p += 1

        for i in range(len(flags)):
            self.flags.append(val[p])
            p += 1

    def createParams(self):
        dict = {"name": self.name, "category": self.category, "type": self.type,
                "lifetime": self.lifetime, "quantmin": self.quantmin,
                "nominal": self.nominal, "cost": self.cost, "quantmax": self.quantmax,
                "min": self.min, "restock": self.restock}

        for u in usages:
            if u in self.usages:
                dict[u] = 1
            else:
                dict[u] = 0

        for t in tiers:
            if t in self.tiers:
                dict[t] = 1
            else:
                dict[t] = 0

        for ta in tags:
            if ta in self.tags:
                dict[ta] = 1
            else:
                dict[ta] = 0

        for i in range(len(self.flags)):
            dict[flags[i]] = self.flags[i]

        self.parameters = dict


def createItemValAndParam():
    # create list with the values of all properties of each item
    itemValues = []
    for myType in types:
        item = Item
        item.fill(myType)
        items.append(item)
        itemValues.append(list(item.parameters.values()))

    # create string for all keys
    params = ""
    for k in items[0].parameters.keys():
        params += k + ", "
    params = params[:-2]

    print(params)
    print(len(items[0].parameters.keys()))


# dbFiller.insertItems(params, itemValues)

def gunsAndMatchingItem(items):
    matching = []
    for i in items:
        if i.type == "gun":
            matches = findMatchingItem(i.name, items)
            for m in matches:
                matching.append((i.name, m))
    return matching

# dbFiller.createCombos(gunsAndMatchingItem(items))


# dbFiller.createCombos(akAttachments(items))
