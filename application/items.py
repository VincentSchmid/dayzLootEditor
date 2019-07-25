import dao
import xmlParser
from xmlParser import isGun, itemTypes, isMag, isAmmo, isOptic

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
        self.rarity = ""
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
        self.type = val[2]
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

        self.rarity = val[p+1]
        self.mod = val[p+2]

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