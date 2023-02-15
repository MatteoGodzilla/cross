from flask import Blueprint,request
import json
from common import URL_PREFIX

customs_create = Blueprint("customs_create",__name__,url_prefix=URL_PREFIX)

# POST /api/v1/customs/create
# Adds a new custom. Values are encoded into the html as json in the same format as "Custom" class
# Should be protected by a user token
@customs_create.route("customs/create",methods=['POST'])
def AddCustom():
    #custom = Custom()
    #return Response(json.dumps(custom,cls=CustomJSONEncoder,indent=4),content_type="application/json")
    return json.dumps(request.headers.__dict__)