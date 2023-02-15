from flask import Blueprint,Response
from database import *
from custom import Custom, CustomJSONEncoder
import json
from common import URL_PREFIX

customs_id = Blueprint("customs_id", __name__, url_prefix=URL_PREFIX)

# GET /api/v1/customs/<id>
# Returns a "Custom" class instance, encoded in json
# <id> refers to the database key in the db, not IDTag
@customs_id.route("customs/<id>")
def GetCustom(id):
    id = int(id)
    if id < 0:
        id *= -1
    conn = CreateConnection()
    if conn is None:
        return "There was an error with connecting to the database (501)"

    InitializeIfNeeded(conn)
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
        return "There was an error trying to get custom {}.".format(id),502