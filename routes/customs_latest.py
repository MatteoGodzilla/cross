from database import *
from fastapi import APIRouter, Response
from common import URL_PREFIX

#customs_latest = Blueprint("customs_latest",__name__,url_prefix=URL_PREFIX)
customs_latest = APIRouter(prefix=URL_PREFIX)

# GET /api/v1/customs/latest/<count>
# returns an array containing ids of the most recent <count> customs in the database
@customs_latest.get("/customs/latest/{count}")
def GetLasts(count:int):
    if count < 0:
        count *= -1

    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    #InitializeIfNeeded(conn)
    cursor = conn.cursor()
    param_query = "SELECT id FROM customs ORDER BY lastUpdate LIMIT ?"
    cursor.execute(param_query, [count])
    res=cursor.fetchall()
    cursor.close()
    DestroyConnection(conn)
    return [ row[0] for row in res ]