try:
    from application import dao
except ModuleNotFoundError:
    import dao

#todo enum from rarities store at one place

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

#input: type to distribute, target nominal, List of include flags
def distribute(type, targetNominal, flags):
    itemsToDistribute = getItems(type)
    numElements = calculateNumElements(itemsToDistribute)
    nominalPerElement = targetNominal / numElements
    setValues(nominalPerElement, itemsToDistribute)

    for item in itemsToDistribute:
        updateDB(item)


def getItems(type):
    global itemsToDistribute
    itemsToDistribute = dao.getItemsToDistibute(type)
    return createListOfDictFromRows(itemsToDistribute)


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
        item["min"] = int(item["nominal"] / 2)
        print(item["name"], item["nominal"], item["min"])
    print("overallNominal", overallNominal)


def updateDB(item):
    for k, v in item.item():
        item[k] = str(v)
    dao.update(item)

def createListOfDictFromRows(itemsToDistribute):
    itemsListOfDicts = []
    keys = dao.returnValues.split(", ")
    for item in itemsToDistribute:
        dict = {}
        for k in range(len(item)):
            dict[keys[k]] = item[k]

        itemsListOfDicts.append(dict)

    return itemsListOfDicts


distribute("gun", 294, 0)
