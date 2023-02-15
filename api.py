from flask import Flask
from routes.customs_create import customs_create
from routes.customs_id import customs_id
from routes.customs_latest import customs_latest

app = Flask(__name__)
app.register_blueprint(customs_create)
app.register_blueprint(customs_id)
app.register_blueprint(customs_latest)

# Default route
@app.route("/")
def default():
    return "Default page"