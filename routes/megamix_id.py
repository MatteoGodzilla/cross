from fastapi import APIRouter,Response, Header
from database import CreateConnection,DestroyConnection,CheckAuth
from megamix import Megamix,CreateMegamix,MegamixToDBColumns, MegamixToDBValues

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
def PatchMegamix(id:int, mgmx:Megamix, authorization:str|None=Header(default=None)) -> Megamix:
    if not CheckAuth(authorization):
        # Convert to raise HTTPException
        return Response("Authorization code was invalid (403)",403)

    if id < 0:
        id *= -1
    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)",500)
    cursor = conn.cursor()
    columns = MegamixToDBColumns(mgmx)
    values = MegamixToDBValues(mgmx)
    values.append(id)

    param_query = "UPDATE megamix SET "
    for i,e in enumerate(columns):
        e = columns[i]
        param_query += e + " = ?"
        if i < len(columns)-1:
            param_query += ", "
    param_query += " WHERE id = ?;"

    print(param_query)
    cursor.execute(param_query, values)
    cursor.close()

    # Set values in megamix-custom
    cursor = conn.cursor()
    query = "DELETE FROM `megamix-customs` WHERE megamixID = ?;"
    cursor.execute(query,[id])

    junction = "INSERT INTO `megamix-customs` (megamixID, customID, `order`) VALUES (?,?,?);"

    rows = []
    for i,customID in enumerate(mgmx.Customs):
        rows.append((id,customID,i))

    cursor.executemany(junction,rows)

    cursor.close()
    conn.commit()
    DestroyConnection(conn)

    return GetMegamix(id)


# DELETE /api/v1/megamix/<id>
# Attempts to delete a megamix already in the database
# Request must have an Authorization code attached to the header, see /api/v1/login
# Returns 204 no content on success
@megamix_id.delete("/{id}")
def DeleteMegamix(id:int, authorization:str|None=Header(default=None)):
    if not CheckAuth(authorization):
        # Convert to raise HTTPException
        return Response("Authorization code was invalid (403)",403)

    if id < 0:
        id *= -1

    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)",500)

    cursor = conn.cursor()
    param_query = 'DELETE FROM megamix WHERE id = ?;'
    checking_query = 'SELECT * FROM megamix WHERE id = ?'
    cursor.execute(param_query, [id])
    cursor.execute(checking_query,[id])
    res = cursor.fetchone()
    cursor.close()

    if res is None:
        conn.commit()
        DestroyConnection(conn)
        return Response(status_code=204)
    else:
        conn.rollback()
        DestroyConnection(conn)
        return Response("There was an error deleting the megamix",501)

