from fastapi import FastAPI
from routes.custom_create import custom_create
from routes.custom_id import custom_id
from routes.custom_latest import custom_latest
from routes.megamix_id import megamix_id
from routes.login import login
from common import URL_PREFIX

app = FastAPI()
app.include_router(custom_create,prefix=URL_PREFIX)
app.include_router(custom_id,prefix=URL_PREFIX)
app.include_router(custom_latest,prefix=URL_PREFIX)
app.include_router(megamix_id,prefix=URL_PREFIX)
app.include_router(login)

# Default route
@app.get("/")
def default():
    return "Default page"
