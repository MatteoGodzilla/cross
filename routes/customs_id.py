from flask import Blueprint,Response, request
from database import *
from custom import Custom, CustomJSONEncoder
import json
from common import URL_PREFIX

customs_id = Blueprint("customs_id", __name__, url_prefix=URL_PREFIX)

# GET /api/v1/customs/<id>
# Returns a "Custom" class instance, encoded in json
# <id> refers to the database key in the db, not IDTag
@customs_id.route("customs/<id>",methods=["GET"])
def GetCustom(id):
    id = int(id)
    if id < 0:
        id *= -1
    conn = CreateConnection()
    if conn is None:
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
        custom = Custom(res)
        return Response(json.dumps(custom,cls=CustomJSONEncoder,indent=4),content_type="application/json")
    else:
        return Response("There was an error trying to get custom {}.".format(id), 500)

# PATCH /api/v1/customs/<id>
# Attempts to change a custom already in the database
# Request must have an Authorization code attached to the header
@customs_id.route("customs/<id>",methods=["PATCH"])
def PatchCustom(id):
    return CheckAuth(request)
    return Response("Not Implemented yet",501)

# DELETE /api/v1/customs/<id>
# Attempts to delete a custom already in the database
# Request must have an Authorization code attached to the header
@customs_id.route("customs/<id>",methods=["DELETE"])
def DeleteCustom(id):
    return Response("Not Implemented yet",501)