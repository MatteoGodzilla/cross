from fastapi import APIRouter,Response
from database import CreateConnection,DestroyConnection
from custom import Megamix,CreateMegamix
from routes.custom_id import GetCustom

megamix_id = APIRouter(prefix="/megamix")

# GET /api/v1/megamix/<id>
# Returns a "Megamix" class instance, encoded in json
# <id> refers to the database key in the db
@megamix_id.get("/{id}")
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

# PATCH /api/v1/megamix/<id>
# Attempts to change a megamix already in the database
# Request must have an Authorization code attached to the header
# Returns a Megamix instance with all of the fields that are currently saved in the db
@megamix_id.patch("/{id}")
def PatchMegamix(id) -> Megamix:
    return Response("NOT IMPLEMENTED",501)

# DELETE /api/v1/megamix/<id>
# Attempts to delete a megamix already in the database
# Request must have an Authorization code attached to the header
# Returns 204 no content on success
@megamix_id.delete("/{id}")
def DeleteMegamix(id):
    return Response("NOT IMPLEMENTED",501)