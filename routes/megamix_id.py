from fastapi import APIRouter,Response, Header
from database import CreateConnection,DestroyConnection,CheckAuth
from megamix import Megamix,CreateMegamix

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

    megamix.Customs = [int(row[0]) for row in res]

    cursor.close()
    DestroyConnection(conn)
    return megamix

# PATCH /api/v1/megamix/<id>
# Attempts to change a megamix already in the database
# Request must have an Authorization code attached to the header, see /api/v1/login
# Returns a Megamix instance with all of the fields that are currently saved in the db
@megamix_id.patch("/{id}")
def PatchMegamix(id, mgmx:Megamix, authorization:str|None=Header(default=None)) -> Megamix:
    if CheckAuth(authorization):
        if id < 0:
            id *= -1
        conn = CreateConnection()
        if conn is None:
            # Convert to raise HTTPException
            return Response("There was an error with connecting to the database (500)",500)
        cursor = conn.cursor()
        values = []
        columns = []
        query = "UPDATE megamix SET "

        if mgmx.Name != "":
            query += "Name = "+ mgmx.Name
        if mgmx.DownloadLink != "":
            query += "DownloadLink = "+ mgmx.DownloadLink
        if mgmx.VideoPreview != "":
            query+= "VideoPreview = "+ mgmx.VideoPreview

        query += "WHERE id = ?;"
        cursor.execute(query, [id])
        cursor.close()
        DestroyConnection(conn)

        return GetMegamix(id)

    else :
        # Convert to raise HTTPException
        return Response("You have to login first",401)

# DELETE /api/v1/megamix/<id>
# Attempts to delete a megamix already in the database
# Request must have an Authorization code attached to the header, see /api/v1/login
# Returns 204 no content on success
@megamix_id.delete("/{id}")
def DeleteMegamix(id, authorization:str|None=Header(default=None)):
    if CheckAuth(authorization):
        if id < 0:
            id *= -1
        conn = CreateConnection()
        if conn is None:
            # Convert to raise HTTPException
            return Response("There was an error with connecting to the database (500)",500)
        cursor = conn.cursor()
        param_query = 'DELETE * FROM megamix WHERE id = ?;'
        checking_query = 'SELECT * FROM megamix-customs WHERE megamixID = ?'
        cursor.execute(param_query, [id])
        cursor.execute(checking_query, [id])
        res = cursor.fetchone()
        cursor.close()
        DestroyConnection(conn)
        if res is None:
            return Response(204)
        else:
            return Response("NOT IMPLEMENTED",501)
    else :
        # Convert to raise HTTPException
        return Response("You have to login first",401)
