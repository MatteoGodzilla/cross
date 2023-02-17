from flask import Blueprint, request, Response
from common import URL_PREFIX
import base64
import bcrypt
import os
import dotenv
from database import *

login = Blueprint("login",__name__,url_prefix=URL_PREFIX)
dotenv.load_dotenv()

@login.route("login")
def basicLogin():
    # The user will send username and password as a basic Authorization header
    authorization = request.headers.get("Authorization")
    if authorization == None:
        return Response("No Authorization header was found",401)

    auth_type,auth_value = authorization.split(" ")
    if auth_type != "Basic":
        return Response("Authorization type must be set to Basic",401)
    if auth_value == None:
        return Response("Authorization type is set to Basic, but no user:password was specified",401)

    # decode auth_value into user and password
    username,clear_password = base64.b64decode(auth_value).decode().split(":")
    #password = bcrypt.hashpw(clear_password.encode(),os.getenv("SALT").encode())

    conn = CreateConnection()
    if conn == None:
        return Response("There was an error with the database",500)

    cursor = conn.cursor()
    query = "SELECT HashedPassword FROM users WHERE Username = ?"

    cursor.execute(query,[username])
    db_password = cursor.fetchone()
    cursor.close()
    DestroyConnection(conn)

    if db_password == None:
        # Username is wrong
        return str(False)

    print(db_password[0])

    if bcrypt.checkpw(clear_password.encode(),str(db_password[0]).encode()):
        # Generate token
        return Response("34567890nyictyonctyontcyno")
    else :
        return Response("Invalid credentials",401)
