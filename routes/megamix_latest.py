from fastapi import APIRouter, Response
from database import CreateConnection, DestroyConnection

megamix_latest = APIRouter()

# GET /api/v1/megamix/latest/<timestamp>
# Return an array of integers containing the most recent megamixes' ids in the database
# A timestamp can be provided in order to return all megamix that are older than the timestamp provided
# if a timestamp is not provided, the current unix time will be used
@megamix_latest.get("/megamix/latest/")
def GetMegamixLatest(timeLimit:int = -1, lastID = -1) -> list[int]:
    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    cursor = conn.cursor()
    param_query = "SELECT id FROM megamix "
    data = []
    if(timeLimit != -1):
        param_query += "WHERE unix_timestamp(lastUpdate) <= ? "
        data.append(timeLimit)
    if(lastID != -1):
        param_query += "WHERE id < ? "
        data.append(timeLimit)

    param_query += "ORDER BY lastUpdate DESC LIMIT 50;"

    cursor.execute(param_query,data)
    res = cursor.fetchall()
    cursor.close()
    DestroyConnection(conn)

    return [row[0] for row in res]