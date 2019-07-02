try:
    from application import dao
except ModuleNotFoundError:
    import dao
from math import ceil

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

rarityMultiplier = {50: 1, 45: 1.5, 40: 2, 35: 2.5, 30: 3, 25: 5, 20: 8, 15: 12, 10: 20}


# todo formula is not clear results are not as expected

# input: type to distribute, target nominal, List of include flags
def distribute(type, targetNominal, targetMag, targetAmmo, flags):
    itemsToDistribute = getItems(type)
    numElements = calculateNumElements(itemsToDistribute)
    nominalPerElement = targetNominal / numElements if numElements != 0 else 0
    setValues(nominalPerElement, itemsToDistribute)

    for item in itemsToDistribute:
        dao.update(item)

    if flags[0] == 1:
        distributeLinkedItem(itemsToDistribute, targetAmmo, "ammo")

    if flags[1] == 1:
        distributeLinkedItem(itemsToDistribute, targetMag, "mag")


def getItems(type):
    global itemsToDistribute
    itemsToDistribute = dao.getItemsToDistibute(type)
    return dao.getDicts(itemsToDistribute)


def calculateNumElements(itemsToDistribute):
    numElements = 0

    for item in itemsToDistribute:
        numElements += rarityMultiplier[item["rarity"]]

    return numElements


def setValues(nominalPerElement, itemsToDistribute):
    for item in itemsToDistribute:
        item["nominal"] = int(round(rarityMultiplier[item["rarity"]] * nominalPerElement))
        item["min"] = int(ceil(item["nominal"] / 2))


def distributeLinkedItem(guns, targetCount, type):
    zeroAllItems(type)
    elementCount = 0
    allItems = dao.getDicts(dao.viewType(type))
    for gun in guns:
        items = []
        elementCount += int(gun["nominal"])
        for corr in dao.getDicts(dao.getWeaponAndCorresponding(gun["name"])):
            if corr["type"] == type:
                for item in allItems:
                    if item["name"] == corr["name"]:
                        items.append(item)

        for item in items:
            item["nominal"] += item["nominal"] / len(items) + 1

    perUnit = targetCount / elementCount if elementCount != 0 else 0

    for item in allItems:
        item["nominal"] = int(ceil(item["nominal"] * perUnit))
        item["min"] = int(ceil(item["nominal"] / 2))

        dao.update(item)


def get_digits(string):
    return int(''.join(filter(lambda x: x.isdigit(), string)))


def zeroAllItems(type):
    for item in dao.getDicts(dao.viewType(type)):
        item["nominal"] = 0
        item["min"] = 0

        dao.update(item)
