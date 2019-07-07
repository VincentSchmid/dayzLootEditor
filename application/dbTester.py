from time import sleep
from os import getcwd
from os.path import abspath
from os.path import join

import dao
import xmlParser


def createDB():
    dao.setConnectionParams("root", "rootroot", "3306", "dayzitems2", "localhost")
    dao.createDB("dayzitems2")
    dao.loadDB(abspath(join(getcwd(), "..", "data", "GENESIS.sql")))


def fillDB():
    params = "name, category, type, lifetime, quantmin, nominal, cost, quantmax, min, restock, Village, Hunting, Police, Office, Medic, Coast, Firefighter, Town, Industrial, Military, Prison, School, Farm, Tier1, Tier2, Tier3, Tier4, shelves, floor, count_in_cargo, count_in_hoarder, count_in_map, count_in_player, crafted, deloot"
    items = []
    items.append(
        ['ACOGOptic', 'weapons', 'optic', '1800', '-1', '5', '100', '-1', '3', '1800', "0", "0", "0", "0", "0", "0",
         "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", '0', '0', '1', '0', '0', '1'])
    items.append(
        ['AK74_Hndgrd', 'weapons', 'attachment', '7200', '-1', '6', '100', '-1', '2', '0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
         0, 0, 0, 0, 0, 0, 0, 0, 0, '0', '0', '1', '0', '0', '0'])
    dao.insertItems(params, items)


#createDB()
#sleep(1)
#fillDB()
all = ["All Items", "All Mods"]
def testGetItems():
    print(dao.getItemsFromCatMods("gun", "MassMany", *all))
    print(dao.getItemsFromCatMods("All Items", "MassMany", *all))
    print(dao.getItemsFromCatMods("ammo", "All Mods", *all))
    print(dao.getItemsFromCatMods("ammo", "MassMany", *all, "12ga"))

    print(dao.getLinkedItems("AKM"))
    print(dao.getWeaponAndCorresponding("AKM"))
    print(dao.getWeaponsFromAccessoire("AmmoBox_556x45Tracer_20Rnd"))

print(len(dao.viewType("gun")))
print(len(xmlParser.itemFromRows(dao.viewType("gun"))))