import redis
import configparser
import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

def task(id):
    while True:
        try:
            messageId = db.brpop(id)
            message = db.get(messageId[1])
            print("posting ", messageId)
            requests.post(id, json=json.loads(message.replace("'", '"')))
            print("completed ", messageId)
        except Exception as e:
            print(f"failure occured: {str(e)}")

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

    consumers = [
            'http://consumer1:5000/consumeEvent', 
            'http://consumer2:5000/consumeEvent', 
            'http://consumer3:5000/consumeEvent']

    with ThreadPoolExecutor(max_workers=len(consumers)) as executor:
            executor.map(task, consumers)