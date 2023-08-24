from database import *
from fastapi import APIRouter, Response
import math

custom_latest = APIRouter()

# GET /api/v1/custom/latest/<timestamp>
# returns an array of integers with the most recent customs' ids in the database
# A timestamp can be provided in order to return all megamix that are older than the timestamp provided
# if a timestamp is not provided, the current unix time will be used
@custom_latest.get("/custom/latest/")
def GetLasts(timeLimit:int = -1, lastID:int = -1) -> list[int]:
    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    cursor = conn.cursor()
    param_query = "SELECT id FROM customs "
    data = []
    if(timeLimit != -1):
        param_query += "WHERE unix_timestamp(lastUpdate) <= ? "
        data.append(math.ceil(timeLimit))
    if(lastID != -1):
        param_query += "WHERE id < ? "
        data.append(lastID)

    param_query += "ORDER BY lastUpdate DESC LIMIT 50"

    cursor.execute(param_query, data)
    res=cursor.fetchall()
    cursor.close()
    DestroyConnection(conn)
    return [ row[0] for row in res ]