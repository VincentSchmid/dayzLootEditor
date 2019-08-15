from os import getcwd
from os.path import abspath
from os.path import join

from time import sleep
import dao
import windows
import pyodbc

def connection(database):
    with pyodbc.connect(
            r'DRIVER={MySQL ODBC 5.3 Unicode Driver};'
            r'UID=root;'
            r'PWD=rootroot;'
            r'PORT=3306;'
            r'DATABASE=' + database + ';'
            r'SERVER=127.0.0.1;'
            r'OPTION=3;'
    ) as connection:
        # Setting Encoding
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setencoding(encoding='utf-8')
        return connection


def createDB(database):
    dao.setConnectionParams("root", "rootroot", "3306", database, "localhost", "5.3")
    dao.createDB("dayzitems5")
    dao.loadDB(windows.getContent(abspath(join(getcwd(), "..", "data", "GENESIS.sql"))))


def fillDB():
    items = []
    items.append(
        ['ACOGOptic', 'weapons', 'optic', '1800', '-1', '5', '100', '-1', '3', '1800', "0", "0", "0", "0", "0", "0",
         "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", '0', '0', '1', '0', '0', '1'])
    items.append(
        ['AK74_Hndgrd', 'weapons', 'attachment', '7200', '-1', '6', '100', '-1', '2', '0', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
         0, 0, 0, 0, 0, 0, 0, 0, 0, '0', '0', '1', '0', '0', '0'])
    dao.insertItems(items)


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

def creating_subTypesTest(dirToTypes, database):
    try:
        createDB(database)
        dao.setColumnNames()
        print(dao.getCoulumNames())
        print("columns:", dao.columns)
        windows.writeTypesToDatabase(dirToTypes)
    finally:
         dao.drop_selected_DB(database)

#creating_subTypesTest(r"C:\Users\puter\OneDrive\Desktop\typesWithClothing.xml")

#print(itm.Item.subTypeCount, itm.Item.itemCount)

def testDaoGetItems(database, dirToTypes):
    try:
        createDB(database)
        sleep(0.05)
        windows.writeTypesToDatabase(dirToTypes)
        cursor = connection(database).cursor()
        cursor.execute("SELECT name from items")
        sleep(0.05)
        print(cursor.fetchall())
    finally:
        pass
        #dao.drop_selected_DB(database)

def testColumnNames(database):
    try:
        createDB(database)
        sleep(0.5)
        cursor = connection(database).cursor()
        cursor.execute("SELECT COLUMN_NAME \
                          FROM INFORMATION_SCHEMA.COLUMNS \
                          WHERE TABLE_SCHEMA= '" + database + "' \
                          AND TABLE_NAME= 'items' \
                          ORDER BY ORDINAL_POSITION;")
        sleep(0.05)
        print([row[0] for row in cursor.fetchall()])
    finally:
        dao.drop_selected_DB(database)


#creating_subTypesTest(r"C:\Program Files (x86)\Steam\steamapps\common\DayZServer\mpmissions\empty.deerisle\db\types.xml")
#testDaoGetItems("dayzitems5", r"C:\Program Files (x86)\Steam\steamapps\common\DayZServer\mpmissions\empty.deerisle\db\types.xml")
#testColumnNames("dayzitems5")

windows.writeToDBFromTrader(r"C:\Program Files (x86)\Steam\steamapps\common\DayZServer\profiles\Trader\TraderConfig.txt")