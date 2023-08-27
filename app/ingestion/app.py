from flask import Flask, request, make_response, Blueprint, g
import json
from utils.queuemanager import DBFactory, DBType

event = Blueprint('event', __name__, url_prefix='/event')
@event.route("/", methods=["POST"])
def ingestEvent():
    contentType = request.headers.get('Content-Type')
    if contentType == 'application/json':
        g.db.push(request.json.__str__(), g.db.getMessageId("pub"))
        return make_response('Accepted', 201)
    else:
        return make_response('Only JSON events are supported', 400)

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    @app.before_request
    def init():
        if 'db' not in g:
            g.db = DBFactory(DBType(app.config['DB_TYPE'])).getInstance(app.config)

    app.register_blueprint(event)
    return app