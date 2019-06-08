import pyodbc
import textwrap

lastQuery = ""


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
        cursor.executemany("insert into items(" + parameters + ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", items)


def createCombos(items):
        cursor = connection().cursor()

        cursor.fast_executemany = True
        cursor.executemany("insert into itemcombos(item1, item2) values (?, ?)", items)


def viewType(type):
    global lastQuery
    lastQuery = "select name, nominal, min, restock, lifetime, type \
        from items \
        where type = '" + type + "';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def viewCategory(category):
    lastQuery = "select name, nominal, min, restock, lifetime, type \
                from items \
                where category = '" + category + "';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def getWeaponAndCorresponding(name):
    lastQuery = "select name, nominal, min, restock, lifetime, type \
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
    lastQuery = "select name, nominal, min, lifetime, restock, type \
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
    lastQuery = "select name, nominal, min, restock, lifetime, type \
                from items \
                WHERE name LIKE '%" + name + "%';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByNameAndType(name, type):
    lastQuery = "select name, nominal, min, restock, lifetime, type \
                from items \
                where type = '" + type + "' \
                and name LIKE '%" + name + "%';"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def searchByNameAndCat(name, cat):
    lastQuery = "select name, nominal, min, restock, lifetime, type \
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
        restock= " + values["restock"] + ", lifetime= " + values["restock"] + " WHERE name = '" + values["name"] + "';")
    conn.commit()

    return reExecuteLastQuery()


def getAllItems():
    cursor = connection().cursor()
    cursor.execute("select * from items")
    return cursor.fetchall()


def reExecuteLastQuery():
    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()
