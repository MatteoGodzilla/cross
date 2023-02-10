# IMPORT of all needed modules
# flask -> Flask : needed to create routes
# flask -> request : needed to get data from url (optional, there are other ways)
# mysql.connector : needed for DB management and interactions
# mysql.connector -> Error : needed to catch DB error (optional, useful)
from flask import Flask
from flask import request
import mysql.connector
from mysql.connector import Error

# SETTING UP THE ROOT FLASK VARIABLE
app = Flask(__name__)

# BUILDING THE DB CONNECTION
def CreateConnection():
    connection = mysql.connector.connect(host='-', database='cross', user='-', password='-')
    if connection.is_connected():
        return connection

# DESTROYING THE DB CONNECTION
def DestroyConnection(connect):
    if connect.is_connected():
        connect.close()

# CHECKING IF THE DB EXISTS - IF NOT, CREATE THE DB AND USE IT
def CheckInit():
    cnn = CreateConnection()
    cursor = cnn.cursor()
    try:
        cursor.execute("SELECT DATABASE 'cross'")
    except Error:
        f = open('./initializeDatabase.sql', 'r')
        readed=""
        for l in f:
            readed+=f.read()
        cursor.execute(readed)
    finally:
        cursor.close()
        cnn.close()

# CREATING ONE SINGLE JSON STRING FROM QUERY RESPONSE
def JSON_Dump(res, cnn):
    cursor = cnn.cursor()
    cursor.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'customs'")
    table_headers = cursor.fetchall()
    json_complete = []
    json = ""
    c = 0

    while c < len(table_headers):
        for (head, r) in (table_headers, res):
            json+="{\'"+head[c]+"\':\'"+r[c]+"\'}"
        c+=1
        json_complete.append(json)
        json = ""
    
    json = ""

    for j in json_complete:
        json += j 

    return json

# GET /api/v1/customs/<id>
# Returns a "Custom" class instance, encoded in json
# <id> refers to the database key in the db, not IDTag
@app.route("/api/v1/customs/<id>")
def GetCustom(id):
    if id < 0:
        id *= -1
    CheckInit()
    conn = CreateConnection()
    cursor = conn.cursor()
    param_query = "SELECT * FROM customs WHERE id = %s"
    cursor.execute(param_query, id)
    res=cursor.fetchall() #fetchall() function give in return a list of lists containing rows content
    cursor.close()
    print(str(res)) #for testing - must remove after
    DestroyConnection(conn)
    return JSON_Dump(res, conn)


# POST /api/v1/customs/add
# Adds a new custom. Values are encoded into the html as json in the same format as "Custom" class
# Should be protected by a user token

# GET /api/v1/customs/latest/<count>
# returns an array containing ids of the most recent <count> customs in the database
@app.route("/api/v1/customs/<count>")
def GetLasts(count):
    if count < 0:
        count *= -1
    CheckInit()
    conn = CreateConnection()
    cursor = conn.cursor()
    param_query = "SELECT id FROM customs ORDER BY lastUpdate LIMIT %s"
    cursor.execute(param_query, count)
    res=cursor.fetchall()
    cursor.close()
    print(str(res)) #for testing - must remove after
    DestroyConnection(conn)
    return JSON_Dump(res, conn)


# TODO: User management