from subprocess import Popen, PIPE

import pyodbc

import categories
import distibutor
import windows

user = ""
pwd = ""
port = ""
database = ""
server = ""
odbcV = ""


def setConnectionParams(username, password, p, dbname, host, odbcVersion):
    windows.writeConfig(username, password, p, dbname, host, odbcVersion)
    global user
    global pwd
    global port
    global database
    global server
    global odbcV

    user = username
    pwd = password
    port = p
    database = dbname
    server = host
    odbcV = odbcVersion


def connection():
    global user
    global pwd
    global port
    global database
    global server
    global odbcV

    if user == "":
        c = windows.readConfig()
        user = c[0]
        pwd = c[1]
        port = c[2]
        database = c[3]
        server = c[4]
        odbcV = c[5]

    with pyodbc.connect(
            r'DRIVER={MySQL ODBC '+odbcV+' Unicode Driver};'
            r'UID=' + user + ';'
            r'PWD=' + pwd + ';'
            r'PORT=' + port + ';'
            r'DATABASE=' + database + ';'
            r'SERVER=' + server + ';'
            r'OPTION=3;'
    ) as connection:
        # Setting Encoding
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setencoding(encoding='utf-8')
        return connection


def getCoulumNames():
    global user
    global pwd
    global port
    global database
    global server
    global odbcV

    if user == "":
        c = windows.readConfig()
        user = c[0]
        pwd = c[1]
        port = c[2]
        database = c[3]
        server = c[4]
        odbcV = c[5]

    cursor = connection().cursor()
    cursor.execute("SELECT COLUMN_NAME \
                      FROM INFORMATION_SCHEMA.COLUMNS \
                      WHERE TABLE_SCHEMA= '" + database + "' \
                      AND TABLE_NAME= 'items' \
                      ORDER BY ORDINAL_POSITION;")
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


def get_all_questionmarks():
    """
    returns a string with a question mark for each column.
    something like: "?, ?, ?"
    """
    questionmarks = ""
    for _ in categories.columns:
        questionmarks += "?, "
    
    return questionmarks[:-2]


def insertItems(params, items):
    conn = connection()
    cursor = conn.cursor()

    cursor.fast_executemany = True
    cursor.executemany(
        f"insert into items({params}) values ({get_all_questionmarks()})",
        items)
    conn.commit()


def insertItem(parameters, item):
    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"insert into items({parameters}) values ({get_all_questionmarks()})",
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
    global user
    global pwd
    global port
    global database
    global server
    global odbcV

    if user == "":
        c = windows.readConfig()
        user = c[0]
        pwd = c[1]
        port = c[2]
        database = c[3]
        server = c[4]
        odbcV = c[5]

    try:
        pyodbc.connect(
            r'DRIVER={MySQL ODBC 5.3 Unicode Driver};'
            r'UID=' + user + ';'
            r'PWD=' + pwd + ';'
            r'PORT=' + port + ';'
            r'SERVER=' + server + ';'
            r'OPTION=3;'
        )
    except pyodbc.Error:
        pyodbc.connect(
            r'DRIVER={MySQL ODBC 8.0 Unicode Driver};'
            r'UID=' + user + ';'
            r'PWD=' + pwd + ';'
            r'PORT=' + port + ';'
            r'SERVER=' + server + ';'
            r'OPTION=3;'
        )
        windows.writeConfig(user, pwd, port, database,server, "8.0")

    with pyodbc.connect(
            r'DRIVER={MySQL ODBC '+odbcV+' Unicode Driver};'
            r'UID=' + user + ';'
            r'PWD=' + pwd + ';'
            r'PORT=' + port + ';'
            r'SERVER=' + server + ';'
            r'OPTION=3;'
    ) as connection:
        # Setting Encoding
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setencoding(encoding='utf-8')

        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE " + name + ";")


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
    cursor = connection().cursor()
    cursor.execute("select @@basedir")
    return cursor.fetchval()


def reExecuteLastQuery():
    global lastQuery
    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def backupDatabase(file=None):
    global user
    global pwd
    global port
    global database
    global server

    if user == "":
        c = windows.readConfig()
        user = c[0]
        pwd = c[1]
        port = c[2]
        database = c[3]
        server = c[4]

    path = getPath() + "bin\\"
    cmdL1 = [path + "mysqldump", "--port=" + port, "-h" + server, "--force", "-u" + user, "-p" + pwd, database]
    p1 = Popen(cmdL1, shell=True, stdout=PIPE)
    if file is not None:
        file.write(p1.communicate()[0])
        file.close()

    if file is None:
        return p1.communicate()[0]


def addColumns():
    query = "ALTER TABLE `" + windows.readConfig()[3] + "`.`items` \
ADD COLUMN `subtype` VARCHAR(45) NULL DEFAULT NULL AFTER `mods`, \
ADD COLUMN `buyprice` INT(11) NULL DEFAULT NULL AFTER `subtype`,\
ADD COLUMN `sellprice` INT(11) NULL DEFAULT NULL AFTER `buyprice`, \
ADD COLUMN `traderCat` VARCHAR(3) NULL DEFAULT NULL AFTER `sellprice`,\
ADD COLUMN `traderExclude` TINYINT(1) UNSIGNED ZEROFILL NOT NULL DEFAULT '0' AFTER `traderCat`;"

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def addNewConstraints():
    query = "ALTER TABLE `itemcombo`\
    DROP FOREIGN KEY `itemcombos_ibfk_1`;\
ALTER TABLE `itemcombo`\
DROP FOREIGN KEY `itemcombos_ibfk_2`;\
ALTER TABLE `itemcombos`\
ADD CONSTRAINT `itemcombos_ibfk_3` \
    FOREIGN KEY (`item1`) REFERENCES `items` (`name`) \
    ON DELETE CASCADE; \
ALTER TABLE `itemcombos` \
    ADD CONSTRAINT `itemcombos_ibfk_4` \
    FOREIGN KEY (`item2`) REFERENCES `items` (`name`) \
    ON DELETE CASCADE;"

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def dropDB():
    global database
    if database == "":
        database = windows.readConfig()[3]

    return drop_selected_DB(database)


def drop_selected_DB(database):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DROP SCHEMA " + database)
    conn.commit()
    return database


def loadDB():
    loadDB(windows.getContent(windows.openFile("sql")))


def loadDB(content):
    global user
    global pwd
    global port
    global database
    global server

    if user == "":
        c = windows.readConfig()
        user = c[0]
        pwd = c[1]
        p = c[2]
        database = c[3]
        server = c[4]

    path = getPath() + "bin\\"

    process = Popen(
        "\"" + path + "mysql\" -u " + user + " -p" + pwd + " -h" + server + " --port " + port + " --default-character-set=utf8 " + database,
        shell=True, stdin=PIPE)
    process.stdin.write(content)
    process.stdin.close()
    process.kill()

def getOdbcVersion():
    try:
        pyodbc.connect(
            r'DRIVER={MySQL ODBC 5.3 Unicode Driver};'
            r'UID=' + user + ';'
            r'PWD=' + pwd + ';'
            r'PORT=' + port + ';'
            r'SERVER=' + server + ';'
            r'OPTION=3;'
        )
        return "5.3"
    except pyodbc.Error:
        pyodbc.connect(
            r'DRIVER={MySQL ODBC 8.0 Unicode Driver};'
            r'UID=' + user + ';'
            r'PWD=' + pwd + ';'
            r'PORT=' + port + ';'
            r'SERVER=' + server + ';'
            r'OPTION=3;'
        )
        windows.writeConfig(user, pwd, port, database,server, "8.0")
        return "8.0"
