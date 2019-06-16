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

rarityMultiplier = {50: 1, 45: 1.5, 40: 2, 35: 2.5, 30: 3, 25: 5, 20: 8, 15: 12, 10: 20}


# todo formula is not clear results are not as expected

# input: type to distribute, target nominal, List of include flags
def distribute(type, targetNominal, targetMag, flags):
    itemsToDistribute = getItems(type)
    numElements = calculateNumElements(itemsToDistribute)
    nominalPerElement = targetNominal / numElements
    setValues(nominalPerElement, itemsToDistribute)

    for item in itemsToDistribute:
        print(item["name"], item["nominal"])
        dao.update(item)

    if flags[0] == 1:
        pass

    if flags[1] == 1:
        distributeMags(itemsToDistribute, targetMag)


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
    for item in itemsToDistribute:
        item["nominal"] = int(round(rarityMultiplier[item["rarity"]] * nominalPerElement))
        item["min"] = int(math.ceil(item["nominal"] / 2))


def getDicts(itemsToDistribute):
    itemsListOfDicts = []
    keys = dao.returnValues.split(", ")
    for item in itemsToDistribute:
        dict = {}
        for k in range(len(item)):
            dict[keys[k]] = item[k]

        itemsListOfDicts.append(dict)

    return itemsListOfDicts


def distributeMags(guns, targetMag):
    zeroAllMags()
    elementCount = 0
    allMags = getDicts(dao.viewType("mag"))
    for item in guns:
        mags = []
        elementCount += int(item["nominal"])
        for corr in getDicts(dao.getWeaponAndCorresponding(item["name"])):
            if corr["type"] == "mag":
                for mag in allMags:
                    if mag["name"] == corr["name"]:
                        mags.append(mag)

        for mag in mags:
            mag["nominal"] += item["nominal"] / len(mags) + 1

    perUnit = targetMag / elementCount

    for mag in allMags:
        mag["nominal"] = int(math.ceil(mag["nominal"] * perUnit))
        mag["min"] = int(math.ceil(mag["nominal"] / 2))

        dao.update(mag)


def get_digits(string):
    return int(''.join(filter(lambda x: x.isdigit(), string)))


def zeroAllMags():
    for mag in getDicts(dao.viewType("mag")):
        mag["nominal"] = 0
        mag["min"] = 0

        dao.update(mag)
