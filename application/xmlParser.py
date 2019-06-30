import xml.etree.ElementTree as ET

items = []

itemTypes = ["gun", "ammo", "optic", "mag", "attachment"]

categories = ["weapons", "containers", "clothes", "food", "tools", "vehiclesparts"]

selection = itemTypes + categories
selection.append("all items")

usages = ["Military",
          "Prison",
          "School",
          "Coast",
          "Village",
          "Industrial",
          "Medic",
          "Police",
          "Hunting",
          "Town",
          "Farm",
          "Firefighter",
          "Office"]

usagesAbr = ["Mil.",
          "Pris.",
          "School",
          "Coast",
          "Vil.",
          "Ind.",
          "Med.",
          "Pol.",
          "Hunt.",
          "Town",
          "Farm",
          "Firef.",
          "Office"]

tiers = ["Tier1", "Tier2", "Tier3", "Tier4"]

tags = ["shelves", "floor"]

flags = ["count_in_cargo",
         "count_in_hoarder",
         "count_in_map",
         "count_in_player",
         "crafted",
         "deloot"]


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
    item = Item()
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


# returns item type of given name if category is weapon else returns category
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


def removeModPrefixes(name):
    modPrefixes = ["Mass", "GP_", "gp_", "FP4_"]

    for prefix in modPrefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name


# checks name if isGun
def isGun(name):
    isGun = True

    name = removeModPrefixes(name)

    paintKeyWords = ["camo", "black", "green", "desert"]
    notGunKeyWords = ["lrs", "ammo", "optic", "sawed", "suppressor", "goggles", "mag", "light", "rnd", "bttstck",
                      "buttstock", "handguard", "hndgrd", "bayonet", "railatt", "compensator", "drum"]

    for keyword in notGunKeyWords:
        if keyword in name.lower():
            isGun = False
            break

    return isGun


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


class Item:
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
        self.mod = ""

    # fills item values based on given type xml block
    def fill(self, xml, mod):
        self.name = xml.attrib["name"]
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
        self.mod = mod
        self.createParams()

    # fills item values based on list of raw values
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

    # creates dictonary of item values and fills them
    def createParams(self):
        dict = {"name": self.name, "category": self.category, "type": self.type,
                "lifetime": self.lifetime, "quantmin": self.quantmin,
                "nominal": self.nominal, "cost": self.cost, "quantmax": self.quantmax,
                "min": self.min, "restock": self.restock, "mods": self.mod}

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

    def getXML(self):
        type = ""
        craftable = False

        if self.flags[-2] == 1:
            craftable = True

        type += "  <type name=\"{}\">\n".format(self.name)
        if not craftable:
            type += "    <nominal>{}</nominal>\n".format(self.nominal)
        type += "    <lifetime>{}</lifetime>\n".format(self.lifetime)
        if not craftable:
            type += "    <min>{}</min>\n".format(self.min)
            type += "    <quantmin>{}</quantmin>\n".format(self.quantmin)
            type += "    <quantmax>{}</quantmax>\n".format(self.quantmax)
            type += "    <cost>{}</cost>\n".format(self.cost)
        type += """    <flags count_in_cargo=\"{}\" count_in_hoarder=\"{}\" count_in_map=\"{}\" count_in_player=\"{}\" crafted=\"{}\" deloot=\"{}\" />\n""" \
            .format(*self.flags)
        if not craftable:
            type += "    <category name=\"{}\"/>\n".format(self.category)
            for usage in self.usages:
                type += "    <usage name=\"{}\"/>\n".format(usage)
            for tier in self.tiers:
                type += "    <value name=\"{}\"/>\n".format(tier)
        type += "  </type>\n"

        return type


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
