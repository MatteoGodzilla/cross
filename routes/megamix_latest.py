from fastapi import APIRouter, Response
from database import CreateConnection, DestroyConnection

megamix_latest = APIRouter()

@megamix_latest.get("/megamix/latest/{count}")
def GetMegamixLatest(count:int):
    count = abs(count)
    conn = CreateConnection()
    if conn is None:
        # Convert to raise HTTPException
        return Response("There was an error with connecting to the database (500)", 500)

    cursor = conn.cursor()
    query = "SELECT id FROM megamix ORDER BY lastUpdate DESC LIMIT ?;"
    cursor.execute(query,[count])
    res = cursor.fetchall()

    ids = [row[0] for row in res]

    DestroyConnection(conn)
    return ids