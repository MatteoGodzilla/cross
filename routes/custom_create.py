from typing import Any
#from flask import Blueprint,request, Response
from fastapi import APIRouter,Response,Header
from common import URL_PREFIX,CUSTOMS_TAG
from database import *
from custom import Custom,CustomToDBColumns,CustomToDBValues

#customs_create = Blueprint("customs_create",__name__,url_prefix=URL_PREFIX)
custom_create = APIRouter(prefix=URL_PREFIX)

# POST /api/v1/custom/create
# Attempts to add a new custom. Values are encoded into the html as json in the same format as "Custom" class
# Request must have an Authorization code attached to the header
@custom_create.post("/custom/create",tags=CUSTOMS_TAG)
def AddCustom(custom:Custom,authorization:str|None = Header(default=None)) -> int:
    if authorization == None:
        # Convert to raise HTTPException
        return Response("No Authorization code was specified (400)", 400)

    #if not CheckAuth(authorization):
    #    # Convert to raise HTTPException
    #    return Response("Invalid Authorization code (401)", 401)

    connection = CreateConnection()
    if connection is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    # Database here is connected

    #if not request.is_json:
    #    # Convert to raise HTTPException
    #    return Response("Payload provided is not a valid json object. Make sure to set the Content-Type to 'application/json' (400)",400)

    # Payload is a valid json object
    IDTag = custom.IDTag

    if IDTag == None:
        # Convert to raise HTTPException
        return Response("A Custom must contain at least an IDTag (400)", 400)
    #IDTag is at least something

    cursor = connection.cursor()
    query = "SELECT IDTag FROM customs WHERE IDTag = ?"
    cursor.execute(query,[IDTag])
    res = cursor.fetchone()
    cursor.close()

    if res != None:
        # Convert to raise HTTPException
        return Response(f"A custom with the IDTag {IDTag} already exists. Multiples are not allowed (400)",400)

    # IDTag is new and valid

    # All fields except IDTag are not mandatory, but that creates a problem:
    # we have to build a query dynamically based on the provided parameters, so that
    # the ones not specified can be defaulted by the database itself

    columns = CustomToDBColumns(custom)
    data = CustomToDBValues(custom)

    #f = open('./AddCustom.sql', 'r')
    ## read all of the file into script
    #query = "".join(f.readlines())

    query = f"INSERT INTO customs ({','.join(columns)}) VALUES ({stringify(data)});"

    cursor = connection.cursor()
    cursor.execute(query,data)
    connection.commit()
    cursor.close()

    lastID = "SELECT LAST_INSERT_ID();"
    cursor = connection.cursor()
    cursor.execute(lastID)
    res = cursor.fetchone()
    print(res[0])
    cursor.close()
    DestroyConnection(connection)
    return Response(str(res[0]),201)

def stringify(list:list[Any]) -> str:
    res = ""
    for i in range(len(list)):
        item = list[i]
        # write actual value
        if item != None:
            if type(item) == str:
                res += '"' + item + '"'
            else:
                res += str(item)

        if i != len(list) - 1:
            res += ","
    return res
