from fastapi import APIRouter, Response,Header, Depends
from fastapi.security import HTTPBasic,HTTPBasicCredentials
import bcrypt
import uuid
from database import *
from datetime import datetime,timedelta
import time

login = APIRouter()
security = HTTPBasic()

# GET /api/v1/login
# The request must contain an 'Authorization: Basic' header containing name and password encoded as base64
# If login is successfull, returns a temporary uuid code that can be used for routes that require authentication
@login.get("/login")
def BasicLogin(credentials:HTTPBasicCredentials = Depends(security)) -> str:
    conn = CreateConnection()
    if conn == None:
        # Convert to raise HTTPException
        return Response("There was an error with the database (not connected)",500)

    cursor = conn.cursor()
    query = "SELECT id, HashedPassword FROM users WHERE Username = ?"

    cursor.execute(query,[credentials.username])
    res = cursor.fetchone()
    if res == None:
        # Convert to raise HTTPException
        return Response("Invalid Credentials",401)
    userID, db_password = res

    if db_password == None:
        # Username is wrong
        return str(False)

    # Clear expired tokens from auth table
    sql = "DELETE FROM auth where Expires < Now();"
    cursor.execute(sql)

    if bcrypt.checkpw(credentials.password.encode(),str(db_password).encode()):
        # Generate token

        code = str(uuid.uuid4())
        # By default the token provided works for up to 2 hours
        # 2 hours = 2*60*60
        now = datetime.now().replace(microsecond=0)
        expires = now + timedelta(hours=2)

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

# GET /api/v1/login/check
# The request must contain an 'Authorization: Bearer' header containing a code to check
@login.get("/login/check")
def checkLogin(authorization:str|None = Header(default=None)):
    return CheckAuth(authorization)
