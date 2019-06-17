from subprocess import Popen, PIPE

import pyodbc

try:
    from application import windows
except ModuleNotFoundError:
    import windows

returnValues = "name,category,type,lifetime,quantmin,nominal,cost," \
               "quantmax,min,restock,Military,Prison,School,Coast,Village," \
               "Industrial,Medic,Police,Hunting,Town,Farm,Firefighter,Office," \
               "Tier1,Tier2,Tier3,Tier4,shelves,floor," \
               "count_in_cargo,count_in_hoarder,count_in_map,count_in_player," \
               "crafted,deloot,ingameName,rarity"

lastQuery = "select " + returnValues + " from items"

user = ""
pwd = ""
port = ""
database = ""
server = ""


def setConnectionParams(username, password, p, dbname, host):
    windows.writeConfig(username, password, p, dbname, host)
    global user
    global pwd
    global port
    global database
    global server
    user = username
    pwd = password
    port = p
    database = dbname
    server = host


def connection():
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

    with pyodbc.connect(
            r'DRIVER={MySQL ODBC 5.3 Unicode Driver};'
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


def insertItems(parameters, items):
    conn = connection()
    cursor = conn.cursor()

    cursor.fast_executemany = True
    cursor.executemany(
        "insert into items(" + parameters + ") values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        items)
    conn.commit()


def createCombos(items):
    conn = connection()
    cursor = conn.cursor()

    cursor.fast_executemany = True
    cursor.executemany("insert into itemcombos(item1, item2) values (?, ?)", items)
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


def getWeaponAndCorresponding(name):
    global lastQuery
    lastQuery = "select * \
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
    lastQuery = "select * \
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
    cursor.execute("UPDATE items SET nominal = " + str(values["nominal"]) + ", min= " + str(values["min"]) + ", \
        restock= " + str(values["restock"]) + ", lifetime= " + str(values["lifetime"]) + ", \
        rarity=" + str(values["rarity"]) + " WHERE name = '" + str(
        values["name"]) + "';")
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


def getAllItems():
    global lastQuery
    lastQuery = "select * from items"

    cursor = connection().cursor()
    cursor.execute(lastQuery)
    return cursor.fetchall()


def createDB(name):
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

    with pyodbc.connect(
            r'DRIVER={MySQL ODBC 5.3 Unicode Driver};'
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
    cmdL1 = [path + "mysqldump", "--port=" + port, "--force", "-u" + user, "-p" + pwd, database]
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
    process = Popen("mysql -u " + user + " -p" + pwd + " -h " + server + " --default-character-set=utf8 " + database,
                    shell=True, stdin=PIPE)
    process.stdin.write(open(fname, "rb").read())
    process.stdin.close()
    process.kill()
