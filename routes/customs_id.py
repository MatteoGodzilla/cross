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

    #InitializeIfNeeded(conn)
    cursor = conn.cursor()
    param_query = "SELECT * FROM customs WHERE id = ? AND visible = 1"
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
def PatchCustom(id:int,authorization:str|None=Header(default=None)):
    if CheckAuth(authorization):
        return Response("Welcome!")
    else:
        # Convert to raise HTTPException
        return Response("You have to login first",401)

# DELETE /api/v1/customs/<id>
# Attempts to delete a custom already in the database
# Request must have an Authorization code attached to the header
@customs_id.delete("/customs/{id}")
def DeleteCustom(id:int,authorization:str|None=Header(default=None)):
    if CheckAuth(authorization):
        return Response("Welcome!")
    else:
        # Convert to raise HTTPException
        return Response("You have to login first",401)