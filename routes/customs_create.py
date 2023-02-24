from typing import Any
#from flask import Blueprint,request, Response
from fastapi import APIRouter,Response,Header
from common import URL_PREFIX
from database import *
from custom import *

#customs_create = Blueprint("customs_create",__name__,url_prefix=URL_PREFIX)
customs_create = APIRouter(prefix=URL_PREFIX)

# POST /api/v1/customs/create
# Attempts to add a new custom. Values are encoded into the html as json in the same format as "Custom" class
# Request must have an Authorization code attached to the header
@customs_create.post("/customs/create")
def AddCustom(custom:Custom,authorization:str|None = Header(default=None)):
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

    print(custom)

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

    columns = ["IDTag"]
    data = [IDTag]

    buildQuery(columns,data,"BPM",custom.BPM)

    buildQuery(columns,data,"DownloadLink",custom.DownloadLink)

    Songs = custom.Songs
    if Songs != None:
        for i in range(min(3,len(Songs))):
            if Songs[i].name != None:
                buildQuery(columns,data,f"Name{i+1}",Songs[i].name)
            if Songs[i].artist != None:
                buildQuery(columns,data,f"Artist{i+1}",Songs[i].artist)


    buildQuery(columns,data,"Charter",custom.Charter)

    buildQuery(columns,data,"Mixer",custom.Mixer)

    diff = custom.Difficulties
    if diff != None:
        if diff.General != None:
            buildQuery(columns,data,"DiffGeneral",diff.General)
        if diff.Tap != None:
            buildQuery(columns,data,"DiffTap",diff.Tap)
        if diff.Crossfade != None:
            buildQuery(columns,data,"DiffCrossfade",diff.Crossfade)
        if diff.Scratch != None:
            buildQuery(columns,data,"DiffScratch",diff.Scratch)

    Charts = custom.Charts
    if Charts != None:
        if Charts.Beginner != None:
            buildQuery(columns,data,"HasBeginnerChart",Charts.Beginner)
        if Charts.Easy != None:
            buildQuery(columns,data,"HasEasyChart",Charts.Easy)
        if Charts.Medium != None:
            buildQuery(columns,data,"HasMediumChart",Charts.Medium)
        if Charts.Hard != None:
            buildQuery(columns,data,"HasHardChart",Charts.Hard)
        if Charts.Expert != None:
            buildQuery(columns,data,"HasExpertChart",Charts.Expert)

    DeckSpeeds = custom.DeckSpeeds
    if DeckSpeeds != None:
        if DeckSpeeds.Beginner != None:
            buildQuery(columns,data,"DeckSpeedBeginner",DeckSpeeds.Beginner)
        if DeckSpeeds.Easy != None:
            buildQuery(columns,data,"DeckSpeedEasy",DeckSpeeds.Easy)
        if DeckSpeeds.Medium != None:
            buildQuery(columns,data,"DeckSpeedMedium",DeckSpeeds.Medium)
        if DeckSpeeds.Hard != None:
            buildQuery(columns,data,"DeckSpeedHard",DeckSpeeds.Hard)
        if DeckSpeeds.Expert != None:
            buildQuery(columns,data,"DeckSpeedExpert",DeckSpeeds.Expert)

    buildQuery(columns,data,"VideoLink",custom.VideoLink)

    buildQuery(columns,data,"Notes",custom.Notes)

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
    return str(res[0])

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

def buildQuery(columns:list[str],data:list[Any],col_name,obj):
    if obj != None:
        columns.append(col_name)
        data.append(obj)