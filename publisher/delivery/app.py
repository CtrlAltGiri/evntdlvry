import redis
import configparser
import os

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

    print('Hello from delivery')
    while True:
        print(db.brpop(config.get('Redis', 'DBNAME')))