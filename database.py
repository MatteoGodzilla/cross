# API Reference for mariadb
# https://mariadb-corporation.github.io/mariadb-connector-python/
from mariadb import mariadb,Connection
from dotenv import load_dotenv
import os

load_dotenv()

# BUILDING THE DB CONNECTION
def CreateConnection() -> Connection|None:
    try:
        connection = mariadb.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        if connection.open:
            InitializeIfNeeded(connection)
            return connection
        else:
            return None
    except Exception as e:
        print(f"EXCEPTION WHILE CONNECTING TO DB:{e}")
        return None

# DESTROYING THE DB CONNECTION
def DestroyConnection(connect : Connection) -> None:
    if connect.open:
        connect.close()

# CHECKING IF THE DB EXISTS - IF NOT, CREATE THE DB AND USE IT
def InitializeIfNeeded(connection:Connection) -> None:
    cursor = connection.cursor()
    # Create Database
    file = open("./sql/CreateDatabase.sql")
    script = "".join(file.readlines())
    cursor.execute(script)
    file.close()
    connection.select_db("`cross`")

    # Create Customs table
    file = open("./sql/CreateTableCustoms.sql")
    script = "".join(file.readlines())
    cursor.execute(script)
    file.close()

    # Create Users table
    file = open("./sql/CreateTableUsers.sql")
    script = "".join(file.readlines())
    cursor.execute(script)
    file.close()

    # Create Users table
    file = open("./sql/CreateTableAuth.sql")
    script = "".join(file.readlines())
    cursor.execute(script)
    file.close()

    cursor.close()
    print("Database Ready")

# Returns true if the 'Authorization' header contains a valid bearer token
def CheckAuth(authorization:str|None) -> bool:
    if authorization == None:
        return False

    auth_type,auth_value = authorization.split(" ")
    if auth_type != "Bearer":
        # Wrong Auth type
        return False
    if auth_value == None:
        # No code specified
        return False

    connection = CreateConnection()
    cursor = connection.cursor()

    sql = "SELECT id FROM auth WHERE code = ? AND Expires > now();"
    cursor.execute(sql,[auth_value])
    res = cursor.fetchone()
    cursor.close()
    DestroyConnection(connection)
    return res != None

#USED TO CHECK THE EXISTENCE OF ONE RESOURCE - At the moment only for customs table
def CheckExistence(conn, id):
    crsr = conn.cursor()
    param_query = "SELECT * FROM customs WHERE id = ?;"
    crsr.execute(param_query, [id])
    res = crsr.fetchone()
    crsr.close()
    if res is None:
        return 0
    else:
        return 1
