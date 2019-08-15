import dao
import items as itms
from windows import getContent

def addColumns():
    dao.addColumns()


def upgrade():
    lines = dao.backupDatabase().decode("utf-8")
    dbName = dao.dropDB()
    dao.createDB(dbName)
    lines = lines.split("\n")

    for i in range(len(lines)):
        if "CONSTRAINT `itemcombos_ibfk_1`" in lines[i]:
            print("yay")
            lines[i] = "CONSTRAINT `itemcombos_ibfk_3` FOREIGN KEY (`item1`) REFERENCES `items` (`name`) ON DELETE CASCADE,\r"
        elif "CONSTRAINT `itemcombos_ibfk_2`" in lines[i]:
            lines[i] = "CONSTRAINT `itemcombos_ibfk_4` FOREIGN KEY (`item2`) REFERENCES `items` (`name`) ON DELETE CASCADE\r"

    newLines = ""
    for line in lines:
        newLines += line + "\n"

    dao.loadDB("".join(newLines).encode('utf-8'))


def findSubTypes(rows):
    itemsWithSubtypes = []
    for row in rows:
        item = itms.Item()
        item.fillFromVal(row)
        item.subtype = itms.findSubType(item.name, item.category, item.type)
        itemsWithSubtypes.append([item.subtype, item.name])

    dao.setSubtypesMany(itemsWithSubtypes)
