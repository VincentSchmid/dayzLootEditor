import dao
import items as itms
import xmlWriter


def addColumns():
    dao.addColumns()


def findSubTypes(rows):
    itemsWithSubtypes = []
    for row in rows:
        item = itms.Item()
        item.fillFromVal(row)
        item.subtype = itms.findSubType(item.name, item.category, item.type)
        itemsWithSubtypes.append([item.subtype, item.name])

    dao.setSubtypesMany(itemsWithSubtypes)
