from fastapi import APIRouter,Response,Header
from database import *
from custom import CreateCustom,Custom,CustomToDBValues,CustomToDBColumns

custom_id = APIRouter(prefix="/custom")

# GET /api/v1/custom/<id>
# Returns a "Custom" class instance, encoded in json
# <id> refers to the database key in the db, not IDTag
@custom_id.get("/{id}")
def GetCustom(id:int) -> Custom:
    id = abs(id)
    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)",500)

    cursor = conn.cursor()
    param_query = "SELECT * FROM customs WHERE id = ? AND visible = 1;"
    # data parameter has to be either a tuple or a list
    cursor.execute(param_query, [id])
    res=cursor.fetchone()
    cursor.close()
    DestroyConnection(conn)

    if res is not None:
        return CreateCustom(res)
    else:
        # Convert to raise HTTPException
        return Response("There was an error trying to get custom {}.".format(id), 500)

# PATCH /api/v1/custom/<id>
# Attempts to change a custom already in the database
# Request must have an Authorization code attached to the header, see /api/v1/login
# Returns a Custom instance with all of the fields that are currently saved in the db
@custom_id.patch("/{id}")
def PatchCustom(id:int, elem:Custom, authorization:str|None=Header(default=None)) -> Custom:
    if not CheckAuth(authorization):
        # Todo: Convert to HTTPexception
        return Response("Authorization code is invalid (403)", 403)

    conn = CreateConnection()
    if conn is None:
        #Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)",500)
    cursor = conn.cursor()

    param_query = "SELECT * FROM customs WHERE id = ?"
    cursor.execute(param_query, [id])
    old = cursor.fetchone()

    if old == None:
        #Convert to raise HTTPException
        return Response("A Valid custom id must be provided (400)",400)

    # The specified id in the url exists

    try:
        columns = CustomToDBColumns(elem)
        data = CustomToDBValues(elem)

        param_query = "UPDATE customs SET "
        for i,e in enumerate(columns):
            e = columns[i]
            param_query += e + " = ?"
            if i < len(columns)-1:
                param_query += ", "
        param_query += " WHERE id = ?;"

        data.append(id)
        cursor.execute(param_query, data)

        param_query = "SELECT * FROM customs WHERE id = ?"
        cursor.execute(param_query, [id])
        new = cursor.fetchone()

        cursor.close()
        conn.commit()
        DestroyConnection(conn)

        return new
    except:
        conn.rollback()
        DestroyConnection(conn)
        return Response("An error has occurred(500)",500)

# DELETE /api/v1/custom/<id>
# Attempts to delete a custom already in the database
# Request must have an Authorization code attached to the header, see /api/v1/login
# Returns 204 no content on success
@custom_id.delete("/{id}")
def DeleteCustom(id:int,authorization:str|None=Header(default=None)):
    if not CheckAuth(authorization):
        # Convert to raise HTTPException
        return Response("Authorization code is invalid (403)",403)
    conn = CreateConnection()
    if conn is None:
        #Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)",500)

    cursor = conn.cursor()
    param_query = "DELETE FROM customs WHERE id = ?;"
    cursor.execute(param_query, [id])
    cursor.close()

    if CheckExistence(conn, id) == 0:
        conn.commit()
        DestroyConnection(conn)
        return Response(status_code=204)
    else:
        conn.rollback()
        DestroyConnection(conn)
        # Convert to raise HTTPException
        return Response("The deletion process has encountered an exception (500)", 500)

