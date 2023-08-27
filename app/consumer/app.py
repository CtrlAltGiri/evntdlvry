from flask import Flask, request, make_response
import json
import random

app = Flask(__name__)
app.config.from_envvar('CONSUMER_SETTINGS')

@app.route("/consumeEvent", methods=["POST"])
def ingestEvent():
    number = random.uniform(0, 1)
    print(number)
    if number > 0.9:
        return make_response('Accepted', 201)
    else:
        return make_response('Bad', 500)

if __name__ == "__main__":
    app.run(debug=True)