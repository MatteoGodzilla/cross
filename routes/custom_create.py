from typing import Any
from fastapi import APIRouter,Response,Header
from common import CUSTOMS_TAG
from database import *
from custom import Custom,CustomToDBColumns,CustomToDBValues

custom_create = APIRouter()

# POST /api/v1/custom/create
# Attempts to add a new custom. Values are encoded into the html as json in the same format as "Custom" class
# Request must have an Authorization code attached to the header
@custom_create.post("/custom/create",tags=CUSTOMS_TAG,status_code=201)
def AddCustom(custom:Custom,authorization:str|None = Header(default=None)) -> int:
    if authorization == None:
        # Convert to raise HTTPException
        return Response("No Authorization code was specified (400)", 400)

    connection = CreateConnection()
    if connection is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    # Database here is connected

    IDTag = custom.IDTag

    if IDTag == None:
        # Convert to raise HTTPException
        return Response("A Custom must contain at least an IDTag (400)", 400)
    #IDTag is at least something

    cursor = connection.cursor()
    query = "SELECT IDTag FROM customs WHERE IDTag = ?"
    cursor.execute(query,[IDTag])
    res = cursor.fetchone()

    if res != None:
        # Convert to raise HTTPException
        return Response(f"A custom with the IDTag {IDTag} already exists. Multiples are not allowed (400)",400)

    # IDTag is new and valid

    # All fields except IDTag are not mandatory, but that creates a problem:
    # we have to build a query dynamically based on the provided parameters, so that
    # the ones not specified can be defaulted by the database itself

    columns = CustomToDBColumns(custom)
    data = CustomToDBValues(custom)

    query = f"INSERT INTO customs ({','.join(columns)}) VALUES ({stringify(data)});"
    cursor.execute(query,data)

    lastID = "SELECT LAST_INSERT_ID();"
    cursor.execute(lastID)
    res = cursor.fetchone()

    cursor.close()
    connection.commit()
    DestroyConnection(connection)
    return Response(str(res[0]))

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
