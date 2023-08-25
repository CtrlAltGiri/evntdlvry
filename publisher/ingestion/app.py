from flask import Flask, request, make_response
import json
from queuemanager import RedisQueue

app = Flask(__name__)
app.config.from_envvar('INGESTION_SETTINGS')
queueInstance = RedisQueue(app.config)

@app.route("/event", methods=["POST"])
def ingestEvent():
    contentType = request.headers.get('Content-Type')
    if contentType == 'application/json':
        queueInstance.push(request.json.__str__())
        return make_response('Accepted', 201)
    else:
        return make_response('Only JSON events are supported', 400)

if __name__ == "__main__":
    # Setup redis
    global db
    db = setup_redis(app.config)

    app.run(debug=True)