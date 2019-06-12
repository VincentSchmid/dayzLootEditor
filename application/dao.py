import pyodbc
import textwrap

returnValues = "name, nominal, min, restock, lifetime, type, rarity"
lastQuery = "select " + returnValues + " from items"


def connection():
    with pyodbc.connect(
            r'DRIVER={MySQL ODBC 5.3 Unicode Driver};'
            r'UID=root;'
            r'PWD=rootroot;'
            r'PORT=3306;'
            r'DATABASE=dayzitems;'
            r'SERVER=127.0.0.1;'
            r'OPTION=3;'
    ) as connection:
        # Setting Encoding
        connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        connection.setencoding(encoding='utf-8')
        return connection


def insertItems(parameters, items):
    cursor = connection().cursor()

    cursor.fast_executemany = True
    cursor.executemany(
        "insert into items(" + parameters + ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        items)


def createCombos(items):
    cursor = connection().cursor()

    cursor.fast_executemany = True
    cursor.executemany("insert into itemcombos(item1, item2) values (?, ?)", items)


def viewType(type):
    global lastQuery
    lastQuery = "select " + returnValues + " \
        from items \
        where type = '" + type + "';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def viewCategory(category):
    global lastQuery
    lastQuery = "select " + returnValues + " \
                from items \
                where category = '" + category + "';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getWeaponAndCorresponding(name):
    global lastQuery
    lastQuery = "select " + returnValues + " \
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
    lastQuery = "select " + returnValues + " \
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
    lastQuery = "select " + returnValues + " \
                from items \
                WHERE name LIKE '%" + name + "%';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByNameAndType(name, type):
    global lastQuery
    lastQuery = "select " + returnValues + " \
                from items \
                where type = '" + type + "' \
                and name LIKE '%" + name + "%';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByNameAndCat(name, cat):
    global lastQuery
    lastQuery = "select " + returnValues + " \
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
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET nominal = " + values["nominal"] + ", min= " + values["min"] + ", \
        restock= " + values["restock"] + ", lifetime= " + values["lifetime"] + ", rarity=" + values[
        "rarity"] + " WHERE name = '" + values["name"] + "';")
    conn.commit()

def updateMany(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cursor.executemany("UPDATE items SET nominal = ?, min= ?, \
        restock= ?, lifetime= ?, rarity= ? WHERE name = ?;", items)


def getItemsToDistibute(type):
    cursor = connection().cursor()
    cursor.execute("select " + returnValues + " from items where type = '" + type + "' and rarity <> 'undefined'")
    return cursor.fetchall()


def getAllItems():
    cursor = connection().cursor()
    cursor.execute("select * from items")
    return cursor.fetchall()


def getPath():
    cursor = connection().cursor()
    cursor.execute("select @@basedir")
    return cursor.fetchval()


def reExecuteLastQuery():
    global lastQuery
    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()
