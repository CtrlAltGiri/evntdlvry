import redis
import configparser
import os
import json
import requests
from utils.retry import Retry
from utils.retrypolicy import RetryPolicy
from concurrent.futures import ThreadPoolExecutor

def preprocess(id):
    newQueue = id + "_processing"
    while db.llen(newQueue) > 0:
        try:
            messageId = db.rpop(newQueue)
            message = db.get(messageId)
            response = requests.post(id, json=json.loads(message.replace("'", '"')))
            response.raise_for_status()
        except:
            print("failed to process message")


def processMessage(id, isRetry):
    newQueue = id + "_processing"
    
    if isRetry:
        messageId = db.brpoplpush(newQueue, newQueue)
    else:
        # spin lock and acquire messages per-consumer
        messageId = db.brpoplpush(id, newQueue)

    message = db.get(messageId)

    print("posting ", messageId, " to consumer ", id)
    response = requests.post(id, json=json.loads(message.replace("'", '"')))
    response.raise_for_status()
    db.brpop(newQueue)
    print("completed ", messageId, " for endpoint ", id, " with response ", response)

def cleanup(id):
    newQueue = id + "_processing"
    print("popping ", db.brpop(newQueue))

if __name__ == "__main__":
    settings = os.environ.get('DELIVERY_SETTINGS')
    config = configparser.ConfigParser()
    config.read(settings)

    db = redis.Redis(
            host=config.get('Redis', 'HOST'),
            port=config.get('Redis', 'PORT'),
            db=config.get('Redis', 'DBNUMBER'),
            password=config.get('Redis', 'PSWRD'),
            decode_responses=True,
        )
    
    db.ping()

    # TODO: Take from discovery service
    consumers = [
            'http://consumer1:5000/consumeEvent', 
            'http://consumer2:5000/consumeEvent', 
            'http://consumer3:5000/consumeEvent']

    rp = RetryPolicy(5, 1.1)
    r = Retry(rp)

    with ThreadPoolExecutor(max_workers=len(consumers)) as executor:
        lambda_preprocess = [(lambda c=c: preprocess(c)) for c in consumers]
        lambda_functions = [(lambda isRetry, c=c: processMessage(c, isRetry)) for c in consumers]
        lambda_cleanups = [(lambda c=c: cleanup(c)) for c in consumers]
        lambda_conditions = [(lambda timesToPerform: True) for c in consumers]
        executor.map(r.run, lambda_conditions, lambda_preprocess, lambda_functions, lambda_cleanups)