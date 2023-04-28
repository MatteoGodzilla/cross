from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from routes.custom_create import custom_create
from routes.custom_id import custom_id
from routes.custom_latest import custom_latest

from routes.megamix_id import megamix_id
from routes.megamix_latest import megamix_latest
from routes.megamix_create import megamix_create

from routes.login import login

version = 1
URL_PREFIX = f"/api/v{version}"
# Tags used to group in the auto generated docs
CUSTOMS_TAG = ["Custom"]
MEGAMIX_TAG = ["Megamix"]
DASHBOARD_URL = "/dashboard"

app = FastAPI(version=version,title="Cross")
app.include_router(custom_create,prefix=URL_PREFIX,tags=CUSTOMS_TAG)
app.include_router(custom_id,prefix=URL_PREFIX,tags=CUSTOMS_TAG)
app.include_router(custom_latest,prefix=URL_PREFIX,tags=CUSTOMS_TAG)

app.include_router(megamix_id,prefix=URL_PREFIX,tags=MEGAMIX_TAG)
app.include_router(megamix_latest,prefix=URL_PREFIX,tags=MEGAMIX_TAG)
app.include_router(megamix_create,prefix=URL_PREFIX,tags=MEGAMIX_TAG)

app.include_router(login,prefix=URL_PREFIX)

app.mount(DASHBOARD_URL,StaticFiles(directory="dashboard"))

# Default route
@app.get("/")
def default():
    return RedirectResponse(DASHBOARD_URL + "/custom/index.html")
