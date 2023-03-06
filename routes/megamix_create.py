from typing import Any
from fastapi import APIRouter, Header, Response
from database import CreateConnection,DestroyConnection

from megamix import Megamix,MegamixToDBColumns,MegamixToDBValues

megamix_create = APIRouter()

@megamix_create.post("/megamix/create")
def CreateMegamix(megamix:Megamix,authorization:str|None = Header(default=None)) -> int:
    if authorization == None:
        # Convert to raise HTTPException
        return Response("No Authorization code was specified (400)", 400)

    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    if len(megamix.Customs) == 0:
        return Response("The name for a megamix cannot be empty (400)", 400)

    if megamix.Name == "":
        return Response("You must provide at least one custom for a megamix (400)", 400)

    cursor = conn.cursor()

    columns = MegamixToDBColumns(megamix)
    values = MegamixToDBValues(megamix)

    # insert to metadata table `megamix`
    query = f"INSERT INTO megamix ({','.join(columns)}) VALUES ({stringify(values)});"
    cursor.execute(query)

    # get the id of this new megamix
    lastID = "SELECT LAST_INSERT_ID();"
    cursor.execute(lastID)
    res = cursor.fetchone()

    junction = "INSERT INTO `megamix-customs` (megamixID, customID, `order`) VALUES (?,?,?);"

    rows = []
    for i,customID in enumerate(megamix.Customs):
        rows.append((res[0],customID,i))

    cursor.executemany(junction,rows)

    cursor.close()
    conn.commit()
    DestroyConnection(conn)
    return Response(str(res[0]),201)

# TODO: this function is duplicated from custom create
# find a better position to put it
def stringify(list:list[Any]) -> str:
    res = ""
    for i,item in enumerate(list):
        # write actual value
        if item != None:
            if type(item) == str:
                res += '"' + item + '"'
            else:
                res += str(item)

        if i != len(list) - 1:
            res += ","
    return res
