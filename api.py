from fastapi import FastAPI
from routes.customs_create import customs_create
from routes.customs_id import customs_id
from routes.customs_latest import customs_latest
from routes.login import login

app = FastAPI()
app.include_router(customs_create)
app.include_router(customs_id)
app.include_router(customs_latest)
app.include_router(login)

# Default route
@app.get("/")
def default():
    return "Default page"
