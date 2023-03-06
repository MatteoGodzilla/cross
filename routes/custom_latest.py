from database import *
from fastapi import APIRouter, Response

custom_latest = APIRouter()

# GET /api/v1/custom/latest/<count>
# returns an array containing ids of the most recent <count> customs in the database
@custom_latest.get("/custom/latest/{count}")
def GetLasts(count:int) -> list[int]:
    count = abs(count)

    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    #InitializeIfNeeded(conn)
    cursor = conn.cursor()
    param_query = "SELECT id FROM customs ORDER BY lastUpdate DESC LIMIT ?"
    cursor.execute(param_query, [count])
    res=cursor.fetchall()
    cursor.close()
    DestroyConnection(conn)
    return [ row[0] for row in res ]