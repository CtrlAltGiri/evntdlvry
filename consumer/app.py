from flask import Flask, request, make_response
import json

app = Flask(__name__)
app.config.from_envvar('CONSUMER_SETTINGS')

@app.route("/consumeEvent", methods=["POST"])
def ingestEvent():
    contentType = request.headers.get('Content-Type')
    if contentType == 'application/json':
        print(request.json)
        return make_response('Accepted', 201)
    else:
        return make_response('Only JSON events are supported', 400)

if __name__ == "__main__":
    app.run(debug=True)