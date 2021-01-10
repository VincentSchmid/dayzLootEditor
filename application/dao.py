from shutil import copyfile
from pathlib import Path
from subprocess import Popen, PIPE

import sqlite3

import categories
import distibutor
import windows

database = "test.db"
databasename = ""


def connection():
    global database
    return sqlite3.connect(database)


def getCoulumNames():
    global database

    if user == "":
        c = windows.readConfig()
        database = c[0]

    cursor = connection().cursor()
    query = "SELECT c.name FROM pragma_table_info('items') c;"
    cursor.execute(query)

    return [row[0] for row in cursor.fetchall()]


columns = ""
lastQuery = "select * from items"


def setColumnNames():
    global columns
    columns = ", ".join(getCoulumNames())


def getDicts(items):
    itemsListOfDicts = []

    for item in items:
        itemsListOfDicts.append(getDict(item))

    return itemsListOfDicts


def getDict(item):
    dict = {}
    keys = getCoulumNames()
    for k in range(len(item)):
        key = keys[k]
        if key == "mods":
            key = "mod"
        if key.startswith("count_in_"):
            key = key[9:]

        dict[key] = item[k]

    return dict


def insertItems(params, items):
    conn = connection()
    cursor = conn.cursor()

    cursor.fast_executemany = True
    cursor.executemany(
        "insert into items(" + params + ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        items)
    conn.commit()


def insertItem(parameters, item):
    conn = connection()
    cursor = conn.cursor()

    print(parameters)
    print(item)

    try:
        cursor.execute(
            "insert into items(" + parameters + ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            item)
        conn.commit()
        return 0
    except pyodbc.IntegrityError:
        return 1


def createCombos(items):
    conn = connection()
    cursor = conn.cursor()

    cursor.fast_executemany = True
    
    #skip empty
    if not items:
        return
    
    cursor.executemany("insert ignore into itemcombos(item1, item2) values (?, ?)", items)
    conn.commit()


def deleteItem(itemName):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE name = ?", itemName)
    conn.commit()


def removeCombo(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM itemcombos WHERE item1 = ? AND item2 = ?", items[0], items[1])
    conn.commit()


def getItemsToZero(names, itemType):
    global lastQuery
    lastQuery = "select * \
                from items \
                where type = '" + itemType + "' \
                and name in ({0})".format(', '.join('?' for _ in names))

    cursor = connection().cursor()
    cursor.execute(lastQuery, names)
    return cursor.fetchall()


def getType(type, subtype=None):
    global lastQuery
    lastQuery = "select * \
                from items \
                where type = '" + type + "'"

    if subtype is not None:
        lastQuery += " and subtype = '" + subtype + "';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getSubtypes():
    cursor = connection().cursor()
    cursor.execute("SELECT subtype FROM items group by subtype")
    return [row[0] if row[0] is not None else "" for row in cursor.fetchall()]


def getSubtypesMods(mod):
    cursor = connection().cursor()
    cursor.execute("SELECT subtype, mods FROM items WHERE mods = ? group by subtype", mod)
    return [_[0] for _ in cursor.fetchall()]


def getCategory(category, subtype=None):
    global lastQuery
    lastQuery = "select * \
                from items \
                where type = '" + category + "'"

    if subtype is not None:
        lastQuery += " and subtype = '" + subtype + "';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()

# name, subtype, tradercat, buyprice, sellprice, rarity, nominal, traderexclude, mods
def getSubtypeForTrader(subtype):
    query = "select name, subtype, tradercat, buyprice, sellprice, rarity, nominal, traderexclude, mods \
                from items \
                where subtype = '" + subtype + "';"

    cursor = connection().cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)):
        if result[i][3] is None:
            result[i][3] = -1
        if result[i][4] is None:
            result[i][4] = -1

        result[i] = list(result[i])

    return result


def getItemsByName(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE name in ({0})\
            AND rarity <> 0".format(', '.join('?' for _ in items)), items)
    return cursor.fetchall()


def setSubtypesMany(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany("UPDATE items SET subtype = ? WHERE name = ?;", items)
    conn.commit()


def setSubtypeForTrader(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany("UPDATE items SET traderCat = ?, buyprice = ?, \
        sellprice= ?, traderExclude= ?, rarity= ? WHERE name = ?;", items)
    conn.commit()


# buyprice, sellprice, tradercat, subtype, name
def setTraderValues(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany(
        "UPDATE IGNORE items SET buyprice = ?, sellprice = ?, traderCat = ?, subtype = ? WHERE name = ?;", items)
    conn.commit()


def getLinkedItems(item):
    items = set()
    cursor = connection().cursor()
    cursor.execute("select * from itemcombos where item1 = ? or item2 = ?", item, item)
    fetched = cursor.fetchall()
    result = []
    for r in fetched:
        result.append(r[1:])

    if result is not None:
        item1 = [row[0] for row in result]
        item2 = [row[1] for row in result]
        for item in item1 + item2:
            items.add(item)
    return items


def getLinekd(name, type):
    if type == "gun" or type == "rifles" or type == "pistols":
        return getWeaponAndCorresponding(name)
    else:
        return getWeaponsFromAccessoire(name)


def getWeaponAndCorresponding(name):
    global lastQuery
    global columns
    lastQuery = "select " + columns + " \
                from items \
                join \
                    (select item2 \
                    FROM (select name, item2 \
                            from items \
                                    join itemcombos i on items.name = i.item1 \
                            where name LIKE '" + name + "') as accessoire \
                    ) as item2 on name = item2.item2 \
                    group by name;"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getWeaponsFromAccessoire(name):
    global lastQuery
    lastQuery = "select " + columns + " \
                from (select item1, item2, items.* \
                      from itemcombos \
                      join items on name = item1 \
                      where item2 LIKE '%" + name + "%' \
                      ) as accessoire \
                      group by name;"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByName(name):
    global lastQuery
    lastQuery = "select * \
                from items \
                WHERE name LIKE '%" + name + "%';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByNameAndType(name, type):
    global lastQuery
    lastQuery = "select * \
                from items \
                where type = '" + type + "' \
                and name LIKE '%" + name + "%';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByNameAndCat(name, cat):
    global lastQuery
    lastQuery = "select * \
                from items \
                where category = '" + cat + "' \
                and name LIKE '%" + name + "%';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getNominalByType(type):
    cursor = connection().cursor()
    cursor.execute(
        "select SUM(nominal) \
        from items \
        where type = ?", type
    )
    global columns
    if columns == "":
        setColumnNames()
    return cursor.fetchval()


def getNominalByUsage(usage):
    cursor = connection().cursor()
    cursor.execute(
        "select SUM(nominal) \
        from items \
        where ? = 1", usage.lower()
    )
    return cursor.fetchval()


def getMinByType(type):
    cursor = connection().cursor()
    cursor.execute(
        "select SUM(min) \
        from items \
        where type = ?", type
    )
    return cursor.fetchval()


def updateType(itemName, type):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET type = ? WHERE name = ?", type, itemName)
    conn.commit()


def updateDropValue(itemName, newValue, valueType):
    if valueType == "rarity":
        updateRarity(itemName, newValue)
    if valueType == "type":
        updateType(itemName, newValue)


def updateRarity(itemName, rarity):
    # todo clean this up
    rarities = distibutor.rarities9
    if rarity in rarities.values():
        for key, value in rarities.items():
            if rarity == value:
                rarity = key

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET rarity = ? WHERE name = ?", rarity, itemName)
    conn.commit()


def update(values):
    query = "UPDATE items SET nominal = " + str(values["nominal"]) + ", min= " + str(values["min"]) + ", \
        restock= " + str(values["restock"]) + ", lifetime= " + str(values["lifetime"]) + ", subtype= '" + str(
        values["subtype"]) + "'" \
            + ", deloot= '" + str(values["deloot"]) + "', mods= '" + str(values["mod"]) + "' WHERE name = '" + str(
        values["name"] + "'")

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    updateFlags(values)

    try:
        updateListValues(values["usage"], values["name"], categories.usages)
    except KeyError:
        pass

    try:
        updateListValues(values["tier"], values["name"], categories.tiers)
    except KeyError:
        pass


def updateFlags(values):
    query = "UPDATE items SET count_in_cargo = ?, count_in_hoarder = ?, count_in_map = ?, count_in_player = ?\
     WHERE name = ?"

    conn = connection()
    cursor = conn.cursor()
    try:
        x = values["cargo"]

    except KeyError:
        values["cargo"] = values["count_in_cargo"]
        values["hoarder"] = values["count_in_hoarder"]
        values["map"] = values["count_in_map"]
        values["player"] = values["count_in_player"]

    cursor.execute(query, values["cargo"], values["hoarder"], values["map"], values["player"], values["name"])
    conn.commit()


def updateMany(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany("UPDATE items SET nominal = ?, min= ?, \
        restock= ?, lifetime= ?, rarity= ? WHERE name = ?;", items)


def getItemsToDistibute(type):
    cursor = connection().cursor()
    cursor.execute("select * from items where type = '" + type + "' and rarity <> 'undefined'")
    return cursor.fetchall()


def getAllItems(subtype=None):
    global lastQuery
    lastQuery = "select * from items"

    if subtype is not None:
        lastQuery += " WHERE subtype = '" + subtype + "'"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getMods():
    cursor = connection().cursor()
    cursor.execute("select mods \
                    from items \
                    group by mods;")
    rows = cursor.fetchall()
    return [row[0] for row in rows]


def getItemsFromCatMods(category, mod, allItems, allMods, search=None):
    search = None if search == "" else search
    query = ""
    if search is not None:
        query += "select name from ("
    query += "select name from items "
    if category != allItems:
        query += "WHERE type = \'{}\' ".format(category)
    if mod != allMods:
        if category != allItems:
            query += "AND "
        else:
            query += "WHERE "
        query += "mods = \'{}\'".format(mod)

    if search is not None:
        query += ") as filtered WHERE name LIKE \'%{}%\';".format(search)

    cursor = connection().cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return [row[0] for row in rows]


def createDB(name):
    global database
    database = name + ".db"

    conn = connection()

    create_items_table = '''CREATE TABLE items
                            (name text NOT NULL PRIMARY KEY,
                            category text NOT NULL,
                            type text NOT NULL,
                            lifetime int NOT NULL,
                            quantmin int NOT NULL,
                            nominal int NOT NULL,
                            cost int NOT NULL,
                            quantmax int NOT NULL,
                            min int NOT NULL,
                            restock int NOT NULL,
                            
                            Military int NOT NULL,
                            Prison int NOT NULL,
                            School int NOT NULL,
                            Coast int NOT NULL,
                            Village int NOT NULL,
                            Industrial int NOT NULL,
                            Medic int NOT NULL,
                            Police int NOT NULL,
                            Hunting int NOT NULL,
                            Town int NOT NULL,
                            Farm int NOT NULL,
                            Firefighter int NOT NULL,
                            Office int NOT NULL,
                            Civilian int NOT NULL,
                            Fishing int NOT NULL,
                            Medical int NOT NULL,

                            Tier1 int NOT NULL,
                            Tier2 int NOT NULL,
                            Tier3 int NOT NULL,
                            Tier4 int NOT NULL,

                            shelves int NOT NULL,
                            floor int NOT NULL,

                            count_in_cargo int NOT NULL,
                            count_in_hoarder int NOT NULL,
                            count_in_map int NOT NULL,
                            count_in_player int NOT NULL,
                            crafted int NOT NULL,
                            deloot int NOT NULL,

                            ingameName text NOT NULL,
                            rarity int mods text NOT NULL,
                            subtype text NOT NULL,
                            buyprice int NOT NULL,
                            sellprice int NOT NULL,
                            traderCat text NOT NULL,
                            traderExclude int)'''
    
    conn.execute(create_items_table)

    query = """CREATE TABLE itemcombos
                (item1 text, item2 text)"""
    
    conn.execute(query)


def getUsages(itemName):
    cursor = connection().cursor()
    cursor.execute("select " + ", ".join(categories.usages) + " from items where name = '" + itemName + "'")
    return cursor.fetchall()[0]


def getTiers(itemName):
    cursor = connection().cursor()
    cursor.execute("select " + ", ".join(categories.tiers) + " from items where name = '" + itemName + "'")
    return cursor.fetchall()[0]


def getRarity(itemName):
    cursor = connection().cursor()
    cursor.execute("select rarity from items where name = ?", itemName)
    return cursor.fetchall()[0][0]


def getSubtype(itemName):
    cursor = connection().cursor()
    cursor.execute("select subtype from items where name = ?", itemName)
    return cursor.fetchval()


def getFlags(itemName):
    cursor = connection().cursor()
    cursor.execute("select count_in_cargo, count_in_hoarder, count_in_map, count_in_player, crafted, deloot \
                    from items where name = ?", itemName)
    return cursor.fetchall()[0]


def getModFromItem(itemName):
    cursor = connection().cursor()
    cursor.execute("SELECT mods FROM items WHERE name = ?", itemName)
    return cursor.fetchall()


def updateListValues(newValues, name, listItems):
    usages = listItems
    query = "UPDATE items SET "
    for i in range(len(usages)):
        query += usages[i] + " = " + str(newValues[i]) + ", "

    query = query[:-2]
    query += " WHERE name = '" + name + "';"

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def getPath():
    global database
    return str(Path(database).absolute().parent.resolve())


def reExecuteLastQuery():
    global lastQuery
    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def backupDatabase(file=None):
    global database
    copyfile(database, database.split(".")[0] + "_backup.db")
