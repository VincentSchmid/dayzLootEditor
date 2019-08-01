import dao
import categories as cat


class Item:
    subTypeCount = 0
    itemCount = 0

    def __init__(self):
        self.name = ""
        self.category = ""
        self.type = ""
        self.subType = ""
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
        self.rarity = ""
        self.mod = ""
        self.buyprice = -1
        self.sellprice = -1
        self.tradercat = "*"
        Item.itemCount += 1

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
        self.subType = findSubType(self.name, self.category, self.type)
        if self.subType is not "":
            Item.subTypeCount += 1
        else:
            pass
        self.mod = mod
        self.createParams()

    # fills item values based on list of raw values
    def fillFromVal(self, val):
        self.name = val[0]
        self.category = val[1]
        self.type = val[2]
        self.lifetime = val[3]
        self.quantmin = val[4]
        self.nominal = val[5]
        self.cost = val[6]
        self.quantmax = val[7]
        self.min = val[8]
        self.restock = val[9]
        p = 10
        for i in range(len(cat.usages)):
            if val[p] == 1:
                self.usages.add(cat.usages[i])
            p += 1

        for i in range(len(cat.tiers)):
            if val[p] == 1:
                self.tiers.add(cat.tiers[i])
            p += 1

        for i in range(len(cat.tags)):
            if val[p] == 1:
                self.tags.add(cat.tags[i])
            p += 1

        for i in range(len(cat.flags)):
            self.flags.append(val[p])
            p += 1

        self.rarity = val[p+1]
        self.mod = val[p+2]
        self.subType = val[p+3]
        self.buyprice = val[p+4]
        self.sellprice = val[p+5]
        self.tradercat = val[p+6]

    # creates dictonary of item values and fills them
    def createParams(self):
        dict = {"name": self.name, "category": self.category, "type": self.type, "subtype": self.subType,
                "lifetime": self.lifetime, "quantmin": self.quantmin, "buyprice": self.buyprice,
                "nominal": self.nominal, "cost": self.cost, "quantmax": self.quantmax, "sellprice": self.sellprice,
                "min": self.min, "restock": self.restock, "mods": self.mod, "tradercat": self.tradercat}

        for u in cat.usages:
            if u in self.usages:
                dict[u] = 1
            else:
                dict[u] = 0

        for t in cat.tiers:
            if t in self.tiers:
                dict[t] = 1
            else:
                dict[t] = 0

        for ta in cat.tags:
            if ta in self.tags:
                dict[ta] = 1
            else:
                dict[ta] = 0

        for i in range(len(self.flags)):
            dict[cat.flags[i]] = self.flags[i]

        self.parameters = dict

    def getXML(self):
        type = ""
        craftable = False

        if self.flags[-2] == 1 or self.nominal == 0:
            craftable = True

        type += "  <type name=\"{}\">\n".format(self.name)
        if not craftable:
            type += "    <nominal>{}</nominal>\n".format(self.nominal)
        type += "    <lifetime>{}</lifetime>\n".format(self.lifetime)
        if not craftable:
            type += "    <restock>{}</restock>\n".format(self.restock)
            type += "    <min>{}</min>\n".format(self.min)
            type += "    <quantmin>{}</quantmin>\n".format(self.quantmin)
            type += "    <quantmax>{}</quantmax>\n".format(self.quantmax)
            type += "    <cost>{}</cost>\n".format(self.cost)
        type += """    <flags count_in_cargo=\"{}\" count_in_hoarder=\"{}\" count_in_map=\"{}\" count_in_player=\"{}\" crafted=\"{}\" deloot=\"{}\" />\n""" \
            .format(*self.flags)
        if not craftable:
            type += "    <category name=\"{}\"/>\n".format(self.category)
            for usage in sorted(self.usages):
                type += "    <usage name=\"{}\"/>\n".format(usage)
            for tier in sorted(self.tiers):
                type += "    <value name=\"{}\"/>\n".format(tier)
        type += "  </type>\n"

        return type

    def getSpawnableTypes(self):
        linkedItems = dao.getLinekd(self.name, self.type)

        magChance= "{:0.2f}".format(0.3)
        opticChance = "{:0.2f}".format(0.10, 2)
        attachmentChance = "{:0.2f}".format(0.20, 2)

        mags = []
        optics = []
        buttstocks = []
        handguards = []
        otherAttachments = []

        for linkedItem in linkedItems:
            if linkedItem.nominal != 0:
                if linkedItem.type == "mag":
                    mags.append(linkedItem)
                if linkedItem.type == "optic":
                    optics.append(linkedItem)
                if linkedItem.type == "attachment":
                    if isHandguard(linkedItem.name):
                        handguards.append(linkedItem)
                    elif isBttStck(linkedItem.name):
                        buttstocks.append(linkedItem)
                    else:
                        otherAttachments.append(linkedItem)

        type = ""

        if self.type == "gun":
            type += "  <type name=\"{}\">\n".format(self.name)

        type += attachmentBlock(mags, magChance)
        type += attachmentBlock(optics, opticChance)
        type += attachmentBlock(handguards, float(1.0))
        type += attachmentBlock(buttstocks, float(1.0))
        type += attachmentBlock(otherAttachments, attachmentChance)

        type += "  </type>\n"

        return type


def attachmentBlock(items, chance):
    type = ""
    if len(items) != 0:
        type += "    <attachments chance=\"{}\">\n".format(chance)
        for item in items:
            type += "      <item name=\"{}\" chance=\"{}\" />\n".format(item.name, round(1.0 / len(items), 2))

        type += "    </attachments>\n"

    return type


# returns item type of given name if category is weapon else returns category
def findType(name, category):
    if category == "weapons":
        if isGun(name):
            return cat.weaponSubTypes[0]

        if isMag(name):
            return cat.weaponSubTypes[3]

        if isAmmo(name):
            return cat.weaponSubTypes[1]

        if isOptic(name):
            return cat.weaponSubTypes[2]

        return cat.weaponSubTypes[4]

    else:
        return category


def findSubType(name, category, itemType):
    if category == "":
        for try_cat in cat.categories:
            result = getKeywordDict(name, try_cat, cat.categoriesDict)
            subType = _subtypeFromDict(result, name)
            if subType is not None:
                return subType

    elif category == "weapon":
        subTypeDict = getKeywordDict(name, itemType, cat.weaponSubTypesDict)
        return _subtypeFromDict(subTypeDict, name)
    else:
        subTypeDict = getKeywordDict(name, category, cat.categoriesDict)
        return _subtypeFromDict(subTypeDict, name)

    return ""


def _subtypeFromDict(subTypeDict, name):
    if subTypeDict is not None:
        for subType, keywords in subTypeDict.items():
            if isSubtype(name, keywords):
                return subType
    return ""


def getKeywordDict(name, superType, nextCat):
    for catName, DictWithKeywords in nextCat.items():
        if catName == superType:
            return DictWithKeywords


def isSubtype(name, keywords):
    for keyword in keywords:
        if keyword in name.lower():
            return True
    return False


def isHandguard(itemName):
    handguardKeyWords = ["handguard", "hndgrd"]
    for kw in handguardKeyWords:
        if kw in itemName.lower():
            return True


def isBttStck(itemName):
    buttstockKeyWords = ["buttstock", "bttstck"]
    for kw in buttstockKeyWords:
        if kw in itemName.lower():
            return True


def isGun(name):
    isGun = True

    name = removeModPrefixes(name)

    paintKeyWords = ["camo", "black", "green", "desert"]
    buttstockKeyWords = ["buttstock", "bttstck"]
    handguardKeyWords = ["handguard", "hndgrd"]
    notGunKeyWords = ["lrs", "ammo", "optic", "sawed", "suppressor", "goggles", "mag", "light", "rnd",
                      "bayonet", "railatt", "compensator", "drum", "palm", "STANAG"] \
                     + buttstockKeyWords + handguardKeyWords

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


def removeModPrefixes(name):
    modPrefixes = ["Mass", "GP_", "gp_", "FP4_"]

    for prefix in modPrefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name
