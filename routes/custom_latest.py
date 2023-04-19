from database import *
from fastapi import APIRouter, Response
import time

custom_latest = APIRouter()

# GET /api/v1/custom/latest/<timestamp>
# returns an array of integers with the most recent customs' ids in the database
# A timestamp can be provided in order to return all megamix that are older than the timestamp provided
# if a timestamp is not provided, the current unix time will be used
@custom_latest.get("/custom/latest/{timeLimit}")
@custom_latest.get("/custom/latest/")
def GetLasts(timeLimit:float = time.time()) -> list[int]:
    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    cursor = conn.cursor()
    param_query = "SELECT id FROM customs WHERE unix_timestamp(lastUpdate) <= ? ORDER BY lastUpdate DESC LIMIT 50"
    cursor.execute(param_query, [timeLimit])
    res=cursor.fetchall()
    cursor.close()
    DestroyConnection(conn)
    return [ row[0] for row in res ]