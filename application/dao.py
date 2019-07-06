from subprocess import Popen, PIPE

import pyodbc

try:
    from application import windows, xmlParser
except ModuleNotFoundError:
    import windows
    import xmlParser

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
    cursor = connection().cursor()
    cursor.execute("""SELECT COLUMN_NAME
                      FROM INFORMATION_SCHEMA.COLUMNS
                      WHERE TABLE_SCHEMA= 'dayzitems'
                      AND TABLE_NAME= 'items';""")
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
        dict[keys[k]] = item[k]

    return dict


def insertItems(parameters, items):
    conn = connection()
    cursor = conn.cursor()

    cursor.fast_executemany = True
    cursor.executemany(
        "insert into items(" + parameters + ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        items)
    conn.commit()


def insertItem(parameters, item):
    conn = connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "insert into items(" + parameters + ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            item)
        conn.commit()
        return 0
    except pyodbc.IntegrityError:
        return 1


def createCombos(items):
    conn = connection()
    cursor = conn.cursor()

    cursor.fast_executemany = True
    cursor.executemany("insert ignore into itemcombos(item1, item2) values (?, ?)", items)
    conn.commit()


def removeCombo(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM itemcombos WHERE item1 = ? AND item2 = ?", items[0], items[1])
    conn.commit()


def viewType(type):
    global lastQuery
    lastQuery = "select * \
                from items \
                where type = '" + type + "';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def viewCategory(category):
    global lastQuery
    lastQuery = "select * \
                from items \
                where category = '" + category + "';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


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
    if type == "gun":
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
                            where name LIKE '%" + name + "%') as accessoire \
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


def update(values):
    query = "UPDATE items SET nominal = " + str(values["nominal"]) + ", min= " + str(values["min"]) + ", \
        restock= " + str(values["restock"]) + ", lifetime= " + str(values["lifetime"]) + ", \
        rarity=" + str(values["rarity"]) + ", deloot= '" + str(values["deloot"]) + "', mods= '" + str(values["mod"]) +\
    "', type= '" + str(values["type"]) + "' WHERE name = '" + str(
        values["name"] + "'")

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    updateListValues(values["usage"], values["name"], xmlParser.usages)
    updateListValues(values["tier"], values["name"], xmlParser.tiers)


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


def getAllItems():
    global lastQuery
    lastQuery = "select * from items"

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
    cursor.execute("select " + ", ".join(xmlParser.usages) + " from items where name = '" + itemName + "'")
    return cursor.fetchall()[0]


def getTiers(itemName):
    cursor = connection().cursor()
    cursor.execute("select " + ", ".join(xmlParser.tiers) + " from items where name = '" + itemName + "'")
    return cursor.fetchall()[0]


def getRarity(itemName):
    cursor = connection().cursor()
    cursor.execute("select rarity from items where name = ?", itemName)
    return cursor.fetchall()[0][0]


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


def backupDatabase(file):
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
    cmdL1 = ["\"" + path + "mysqldump\"", "--port=" + port, "--force", "-u" + user, "-p" + pwd, database]
    p1 = Popen(cmdL1, shell=True, stdout=PIPE)
    file.write(p1.communicate()[0])
    file.close()
    p1.kill()


def loadDB():
    loadDB(windows.openFile("sql"))


def loadDB(fname):
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
        "\"" + path + "mysql\" -u " + user + " -p" + pwd + " -h " + server + " --default-character-set=utf8 " + database,
        shell=True, stdin=PIPE)
    process.stdin.write(open(fname, "rb").read())
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
