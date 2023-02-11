# IMPORT of all needed modules
# flask -> Flask : needed to create routes
# flask -> request : needed to get data from url (optional, there are other ways)
# mariadb : needed for DB management and interactions
# mariadb -> Error : needed to catch DB error (optional, useful)

# API Reference for mariadb
# https://mariadb-corporation.github.io/mariadb-connector-python/

from flask import Flask
from mariadb import mariadb,Error,Connection
from custom import Custom,CustomJSONEncoder
import json

# SETTING UP THE ROOT FLASK VARIABLE
app = Flask(__name__)

# BUILDING THE DB CONNECTION
def CreateConnection() -> Connection|None:
    connection = mariadb.connect(host='34.28.206.168', database='cross', user='remote', password='remotePassword')
    if connection.open:
        return connection
    else:
        return None

# DESTROYING THE DB CONNECTION
def DestroyConnection(connect : Connection) -> None:
    if connect.open:
        connect.close()

# CHECKING IF THE DB EXISTS - IF NOT, CREATE THE DB AND USE IT
def InitializeIfNeeded(connection:Connection) -> None:
    try:
        connection.select_db("`cross`")
        print("Chosen database cross")
    except Error:
        cursor = connection.cursor()
        f = open('./initializeDatabase.sql', 'r')
        # read all of the file into script
        script = "".join(f.readlines())
        cursor.execute(script)
        cursor.close()
        print("Initialized the database")

# GET /api/v1/customs/<id>
# Returns a "Custom" class instance, encoded in json
# <id> refers to the database key in the db, not IDTag
@app.route("/api/v1/customs/<id>")
def GetCustom(id):
    id = int(id)
    if id < 0:
        id *= -1
    conn = CreateConnection()
    if conn is None:
        return "There was an error with connecting to the database (501)"

    InitializeIfNeeded(conn)
    cursor = conn.cursor()
    param_query = "SELECT * FROM customs WHERE id = ? AND visible = 1"
    # data parameter has to be either a tuple or a list
    cursor.execute(param_query, [id])
    res=cursor.fetchone()
    cursor.close()
    DestroyConnection(conn)

    if res is not None:
        custom = Custom(res)
        return json.dumps(custom,cls=CustomJSONEncoder,indent=4)
    else:
        return "There was an error trying to get custom {}.".format(id),501

# POST /api/v1/customs/add
# Adds a new custom. Values are encoded into the html as json in the same format as "Custom" class
# Should be protected by a user token

# GET /api/v1/customs/latest/<count>
# returns an array containing ids of the most recent <count> customs in the database
@app.route("/api/v1/customs/latests/<count>")
def GetLasts(count):
    count = int(count)
    if count < 0:
        count *= -1

    conn = CreateConnection()
    if conn is None:
        return "There was an error with connecting to the database (501)"

    InitializeIfNeeded(conn)
    cursor = conn.cursor()
    param_query = "SELECT id FROM customs ORDER BY lastUpdate LIMIT %s"
    cursor.execute(param_query, count)
    res=cursor.fetchall()
    cursor.close()
    #print(str(res)) #for testing - must remove after
    DestroyConnection(conn)
    return res # temporary

    #return JSON_Dump(res, conn) #for now the function return a json, in the same way GetCustom() logic do

# Default route
@app.route("/")
def default():
    return "Default page"
