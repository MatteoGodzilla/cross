from fastapi import APIRouter,Response,Header
from database import *
from custom import CreateCustom
from common import URL_PREFIX

customs_id = APIRouter(prefix=URL_PREFIX)

# GET /api/v1/customs/<id>
# Returns a "Custom" class instance, encoded in json
# <id> refers to the database key in the db, not IDTag
@customs_id.get("/customs/{id}")
def GetCustom(id:int):
    if id < 0:
        id *= -1
    conn = CreateConnection()
    if conn is None:
        # Convert to HTTPException
        return Response("There was an error with connecting to the database (500)",500)

    # InitializeIfNeeded(conn) - At the moment this function call is useless.
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

# PATCH /api/v1/customs/<id>
# Attempts to change a custom already in the database
# Request must have an Authorization code attached to the header
@customs_id.patch("/customs/{id}")
def PatchCustom(id:int,authorization:str, elem:Custom|None=Header(default=None)):
    if CheckAuth(authorization):
        conn = CreateConnection()
        if conn is None:
            #Convert to HTTPException
            return Response("There was an error with connecting to the database (500)",500)
        cursor = conn.cursor()
        
        param_query = "SELECT * FROM customs WHERE id = ?"
        cursor.execute(param_query, [id])
        old = cursor.fetchone()
       
        new_data = json.loads(elem.json())
        keys = new_data.keys()
        values = new_data.values()
        param_query = "UPDATE customs SET "
        for e in keys:
            param_query += e+"= ?, "
        param_query += ";"
        cursor.execute(param_query, values)
        
        param_query = "SELECT * FROM customs WHERE id = ?"
        cursor.execute(param_query, [id])
        new = cursor.fetchone()
        
        cursor.close()
        DestroyConnection(conn)
        if old == new:
            return Response("An error as occured (500)", 500)
        else:
            return Response("Resources updated successfully (200)", 200)
    else:
        # Convert to raise HTTPException
        return Response("You have to login first",401)
    
# DELETE /api/v1/customs/<id>
# Attempts to delete a custom already in the database
# Request must have an Authorization code attached to the header
@customs_id.delete("/customs/{id}")
def DeleteCustom(id:int,authorization:str|None=Header(default=None)):
    if CheckAuth(authorization):
        conn = CreateConnection()
        if conn is None:
            #Convert to HTTPException
            return Response("There was an error with connecting to the database (500)",500)
        cursor = conn.cursor()
        param_query = "DELETE * FROM customs WHERE id = ?;"
        cursor.execute(param_query, [id])
        cursor.close()
        
        # CheckExistence(conn, id) - Probably useful to check the deletion and the update of one custom
        if CheckExistence(conn, id) == 0:
            DestroyConnection(conn)
            return Response("Resource deleted successfully (204)", 204)
        else:
            DestroyConnection(conn)
            return Response("The deletion process has encountered an exception (501)", 501) #Exception 501 is temporarily
    else:
        # Convert to raise HTTPException
        return Response("You have to login first",401)
