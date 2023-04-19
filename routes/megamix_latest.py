from fastapi import APIRouter, Response
from database import CreateConnection, DestroyConnection
import time

megamix_latest = APIRouter()

# GET /api/v1/megamix/latest/<timestamp>
# Return an array of integers containing the most recent megamixes' ids in the database
# A timestamp can be provided in order to return all megamix that are older than the timestamp provided
# if a timestamp is not provided, the current unix time will be used
@megamix_latest.get("/megamix/latest/{timestamp}")
@megamix_latest.get("/megamix/latest/")
def GetMegamixLatest(timestamp:float = time.time()) -> list[int]:
    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    cursor = conn.cursor()
    query = "SELECT id FROM megamix WHERE unix_timestamp(lastUpdate) <= ? ORDER BY lastUpdate DESC LIMIT 50"
    cursor.execute(query,[timestamp])
    res = cursor.fetchall()

    ids = [row[0] for row in res]

    DestroyConnection(conn)
    return ids