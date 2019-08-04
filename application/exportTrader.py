from windows import addToClipboard
from distibutor import rarityMultiplier

def createTrader(root, subtype, rows):
    text = "	<Category> {}\n".format(subtype)

    for row in rows:
        name = row[0]
        traderCat = row[1]
        buyPrice = row[2]
        sellPrice = row[3]
        excluded = True if row[4] == 1 else False
        if not excluded:
            text += "		{},                 {},         {},         {}\n".format(name, traderCat, buyPrice, sellPrice)
    text += "\n"

    addToClipboard(root, text)

#(rarity, nominal)
def distribute(rows, minBuy, maxBuy, minSell, maxSell, useRarity):

    distribution = getDistribution(rows, useRarity)

    lowestValue = distribution[0]
    for i in range(len(distribution)):
        distribution[i] = distribution[i] - lowestValue

    deltaBuy = maxBuy - minBuy
    deltaSell = maxSell - minSell

    buyPriceForDistrib = dict()
    sellPriceForDistrib = dict()

    for number in distribution:
        buyPriceForDistrib[number + lowestValue] = maxBuy - int(number * deltaBuy / distribution[-1])
        sellPriceForDistrib[number + lowestValue] = maxSell - int(number * deltaSell / distribution[-1])

    buyPriceForDistrib[0] = -1
    sellPriceForDistrib[0] = -1

    return buyPriceForDistrib, sellPriceForDistrib

def getDistribution(rows, rarity_is_set):

    raritySet = set()

    if rarity_is_set:
        for item in rows:
            if item[0] != 0:
                raritySet.add(rarityMultiplier[item[0]])
    else:
        for item in rows:
            raritySet.add(item[1])

    raritySet = sorted(raritySet)
    if 0 in raritySet:
        raritySet.pop(0)

    return raritySet