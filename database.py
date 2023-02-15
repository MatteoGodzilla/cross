# API Reference for mariadb
# https://mariadb-corporation.github.io/mariadb-connector-python/
from mariadb import mariadb,Error,Connection
from dotenv import load_dotenv
import os

load_dotenv()

# BUILDING THE DB CONNECTION
def CreateConnection() -> Connection|None:
    try:
        connection = mariadb.connect(host=os.getenv("DB_HOST"), database='cross', user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
        if connection.open:
            return connection
        else:
            return None
    except:
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
