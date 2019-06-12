try:
    from application import dao
except ModuleNotFoundError:
    import dao
import math

# todo enum from rarities store at one place

rarities9 = {0: "undefined",
             50: "Legendary",
             45: "Extremely Rare",
             40: "Very Rare",
             35: "Rare",
             30: "Somewhat Rare",
             25: "Uncommon",
             20: "Common",
             15: "Very Common",
             10: "All Over The Place"}

rarityMultiplier = {50: 1, 45: 1.5, 40: 2, 35: 2.5, 30: 3, 25: 4, 20: 5, 15: 7.5, 10: 10}


# todo formula is not clear results are not as expected

# input: type to distribute, target nominal, List of include flags
def distribute(type, targetNominal, flags):
    print(flags)
    itemsToDistribute = getItems(type)
    numElements = calculateNumElements(itemsToDistribute)
    nominalPerElement = targetNominal / numElements
    setValues(nominalPerElement, itemsToDistribute)

    for item in itemsToDistribute:
        updateDB(item)

    if flags[0] == 1:
        pass

    if flags[1] == 1:
        distributeMags(itemsToDistribute, nominalPerElement)


def getItems(type):
    global itemsToDistribute
    itemsToDistribute = dao.getItemsToDistibute(type)
    return getDicts(itemsToDistribute)


def calculateNumElements(itemsToDistribute):
    numElements = 0

    for item in itemsToDistribute:
        numElements += rarityMultiplier[item["rarity"]]

    return numElements


def setValues(nominalPerElement, itemsToDistribute):
    overallNominal = 0
    for item in itemsToDistribute:
        item["nominal"] = int(round(rarityMultiplier[item["rarity"]] * nominalPerElement, 0))
        overallNominal += item["nominal"]
        item["min"] = int(math.ceil(item["nominal"] / 2))


def updateDB(item):
    for k, v in item.items():
        item[k] = str(v)
    dao.update(item)


def getDicts(itemsToDistribute):
    itemsListOfDicts = []
    keys = dao.returnValues.split(", ")
    for item in itemsToDistribute:
        dict = {}
        for k in range(len(item)):
            dict[keys[k]] = item[k]

        itemsListOfDicts.append(dict)

    return itemsListOfDicts

def distributeMags(items, nominalPerElement):
    zeroAllMags()
    for item in items:
        for corr in getDicts(dao.getWeaponAndCorresponding(item["name"])):
            if corr["type"] == "mag":
                corr["nominal"] += min(nominalPerElement * int(rarityMultiplier[int(item["rarity"])]), 7)
                corr["min"] += int(math.ceil(int(item["nominal"]) / 2))

                for k, v in corr.items():
                    corr[k] = str(v)

                dao.update(corr)


def zeroAllMags():
    for mag in getDicts(dao.viewType("mag")):
        mag["nominal"] = 0
        mag["min"] = 0

        for k, v in mag.items():
            mag[k] = str(v)

        dao.update(mag)
