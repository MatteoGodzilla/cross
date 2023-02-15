from typing import Any
from flask import Blueprint,request, Response
from common import URL_PREFIX
from database import *
from custom import *

customs_create = Blueprint("customs_create",__name__,url_prefix=URL_PREFIX)

# POST /api/v1/customs/create
# Attempts to add a new custom. Values are encoded into the html as json in the same format as "Custom" class
# Request must have an Authorization code attached to the header
@customs_create.route("customs/create",methods=['POST'])
def AddCustom():
    connection = CreateConnection()
    if connection is None:
        return Response("There was an error with connecting to the database (500)", 500)

    # Database here is connected

    if not request.headers.get("Authorization"):
        return Response("No Authorization code was specified (400)",400)
    # User is authenticated (somehow, need to figure it out in the future)

    if not request.is_json:
        return Response("Payload provided is not a valid json object. Make sure to set the Content-Type to 'application/json' (400)",400)

    # Payload is a valid json object
    IDTag = try_read(request.json,"IDTag")

    if IDTag == None:
        return Response("A Custom must contain at least an IDTag (400)", 400)
    #IDTag is at least something

    cursor = connection.cursor()
    query = "SELECT IDTag FROM customs WHERE IDTag = ?"
    cursor.execute(query,[IDTag])
    res = cursor.fetchone()
    cursor.close()

    if res != None:
        return Response(f"A custom with the IDTag {IDTag} already exists. Multiples are not allowed (400)",400)

    # IDTag is new and valid

    # All fields except IDTag are not mandatory, but that creates a problem:
    # we have to build a query dynamically based on the provided parameters, so that
    # the ones not specified can be defaulted by the database itself

    columns = ["IDTag"]
    data = [IDTag]

    BPM = try_read(request.json,"BPM")
    buildQuery(columns,data,"BPM",BPM)

    DownloadLink = try_read(request.json,"DownloadLink")
    buildQuery(columns,data,"DownloadLink",DownloadLink)

    Songs : list[Song] = try_read(request.json,"Songs")
    if Songs != None:
        for i in range(min(3,len(Songs))):
            if "name" in Songs[i]:
                buildQuery(columns,data,f"Name{i+1}",Songs[i]["name"])
            if "artist" in Songs[i]:
                buildQuery(columns,data,f"Artist{i+1}",Songs[i]["artist"])


    Charter = try_read(request.json,"Charter")
    buildQuery(columns,data,"Charter",Charter)

    Mixer = try_read(request.json,"Mixer")
    buildQuery(columns,data,"Mixer",Mixer)

    Difficulties = try_read(request.json,"Difficulties")
    if Difficulties != None:
        if "General" in Difficulties:
            buildQuery(columns,data,"DiffGeneral",Difficulties["General"])
        if "Tap" in Difficulties:
            buildQuery(columns,data,"DiffTap",Difficulties["Tap"])
        if "Crossfade" in Difficulties:
            buildQuery(columns,data,"DiffCrossfade",Difficulties["Crossfade"])
        if "Scratch" in Difficulties:
            buildQuery(columns,data,"DiffScratch",Difficulties["Scratch"])

    Charts = try_read(request.json,"Charts")
    if Charts != None:
        if "Beginner" in Charts:
            buildQuery(columns,data,"HasBeginnerChart",Charts["Beginner"])
        if "Easy" in Charts:
            buildQuery(columns,data,"HasEasyChart",Charts["Easy"])
        if "Medium" in Charts:
            buildQuery(columns,data,"HasMediumChart",Charts["Medium"])
        if "Hard" in Charts:
            buildQuery(columns,data,"HasHardChart",Charts["Hard"])
        if "Expert" in Charts:
            buildQuery(columns,data,"HasExpertChart",Charts["Expert"])

    DeckSpeeds = try_read(request.json,"DeckSpeeds")
    if DeckSpeeds != None:
        if "Beginner" in DeckSpeeds:
            buildQuery(columns,data,"DeckSpeedBeginner",DeckSpeeds["Beginner"])
        if "Easy" in DeckSpeeds:
            buildQuery(columns,data,"DeckSpeedEasy",DeckSpeeds["Easy"])
        if "Medium" in DeckSpeeds:
            buildQuery(columns,data,"DeckSpeedMedium",DeckSpeeds["Medium"])
        if "Hard" in DeckSpeeds:
            buildQuery(columns,data,"DeckSpeedHard",DeckSpeeds["Hard"])
        if "Expert" in DeckSpeeds:
            buildQuery(columns,data,"DeckSpeedExpert",DeckSpeeds["Expert"])

    VideoLink = try_read(request.json,"VideoLink")
    buildQuery(columns,data,"VideoLink",VideoLink)

    Notes = try_read(request.json,"Notes")
    buildQuery(columns,data,"Notes",Notes)

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

def try_read(json,attribute):
    try:
        return json[attribute]
    except:
        return None

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