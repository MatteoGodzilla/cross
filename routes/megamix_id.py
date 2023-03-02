from fastapi import APIRouter,Response
from database import CreateConnection,DestroyConnection
from custom import Megamix,CreateMegamix
from common import URL_PREFIX
from routes.customs_id import GetCustom

megamix_id = APIRouter(prefix=URL_PREFIX)

@megamix_id.get("/megamix/{id}")
def GetMegamix(id:int) -> Megamix:
    if id < 0:
        id *= -1
    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)",500)

    megamix = Megamix()

    cursor = conn.cursor()
    query = "SELECT * FROM megamix WHERE id = ?;"
    cursor.execute(query,[id])
    res = cursor.fetchone()

    if res is None:
        # Convert to raise HTTPException
        return Response(f"There was an error trying to get megamix {id}.", 500)

    megamix = CreateMegamix(res)

    query = "SELECT customID FROM `megamix-customs` WHERE megamixID = ? ORDER BY `order`;"
    cursor.execute(query,[id])
    res = cursor.fetchall()

    songs = [row[0] for row in res]
    for song in songs:
        custom = GetCustom(song)
        if type(custom) is Response:
            cursor.close()
            DestroyConnection(conn)
            return Response(f"There was an error trying to get customs for megamix {id}.",500)
        megamix.Customs.append(custom)

    cursor.close()
    DestroyConnection(conn)
    return megamix

@megamix_id.patch("/megamix/{id}")
def PatchMegamix(id):
    return Response("NOT IMPLEMENTED",501)

@megamix_id.delete("/megamix/{id}")
def DeleteMegamix(id):
    return Response("NOT IMPLEMENTED",501)