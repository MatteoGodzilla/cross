from fastapi import APIRouter, Response,Header,HTTPException
from common import URL_PREFIX
import base64
import bcrypt
import uuid
from database import *
from datetime import datetime,timezone,timedelta

login = APIRouter(prefix=URL_PREFIX)

@login.get("/login")
def BasicLogin(authorization:str|None = Header(default=None)) -> str:
    # The user will send username and password as a basic Authorization header
    if authorization == None:
        return Response("No Authorization header was found",401)

    auth_type,auth_value = authorization.split(" ")
    if auth_type != "Basic":
        # Convert to raise HTTPException
        return Response("Authorization type must be set to Basic",401)
    if auth_value == None:
        # Convert to raise HTTPException
        return Response("Authorization type is set to Basic, but no user:password was specified",401)

    # decode auth_value into user and password
    username,clear_password = base64.b64decode(auth_value).decode().split(":")

    conn = CreateConnection()
    if conn == None:
        # Convert to raise HTTPException
        return Response("There was an error with the database (not connected)",500)

    cursor = conn.cursor()
    query = "SELECT id, HashedPassword FROM users WHERE Username = ?"

    cursor.execute(query,[username])
    res = cursor.fetchone()
    if res == None:
        # Convert to raise HTTPException
        return Response("There was an error with the database (username not found)",500)
    userID, db_password = res
    cursor.close()

    if db_password == None:
        # Username is wrong
        return str(False)

    if bcrypt.checkpw(clear_password.encode(),str(db_password).encode()):
        # Generate token
        cursor = conn.cursor()

        code = str(uuid.uuid4())
        # By default the token provided works for up to 2 hours
        # 2 hours = 2*60*60
        now = datetime.now(timezone.utc).replace(microsecond=0)
        expires = now + timedelta(hours=2)
        #print(userID)
        #print(code)
        #print(expires)
        sql = "INSERT INTO auth (`User ID`,`Code`,`Expires`) VALUES (?,?,?);"
        cursor.execute(sql,[userID,code,expires])
        cursor.close()
        conn.commit()
        DestroyConnection(conn)

        return code
    else :
        DestroyConnection(conn)
        # Convert to raise HTTPException
        return Response("Invalid credentials",401)
