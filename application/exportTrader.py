from windows import addToClipboard

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
