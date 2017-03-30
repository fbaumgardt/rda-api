from src.app import CollectionsAPI
from flask import send_from_directory
from src.collections.routes import routes as r_collections
from src.members.routes import routes as r_members
from src.service.routes import routes as r_service
from src.utils.errors import activate
from src.utils.json import *
from flask_cors import CORS, cross_origin

app = CollectionsAPI(__name__)
CORS(app)
app.json_encoder = RDAJSONEncoder
app.json_decoder = RDAJSONDecoder
activate(app)


for (url, kwargs) in r_service + r_collections + r_members:
    app.add_url_rule(url, **kwargs)

def index():
    return send_from_directory("www","index.html")
app.add_url_rule("/", methods=["GET"], view_func=index)

def apidocs():
    return send_from_directory("www","swagger.json")
app.add_url_rule("/apidocs", methods=["GET"], view_func=apidocs)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
