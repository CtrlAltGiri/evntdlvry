import redis

class RedisQueue:
    def setup_redis(self, config):
        self.db = redis.Redis(
            host=config["REDIS_HOST"],
            port=config["REDIS_PORT"],
            db=config["REDIS_DBNUMBER"],
            password=config["REDIS_PSWRD"],
            decode_responses=True,
        )

        self.db.ping()
        print('db connection successful')

    def push(self, message):
        self.db.lpush(self.database_name, message)
    
    def pop(self):
        return self.db.lpop(self.database_name)

    def __init__(self, config):
        self.setup_redis(config)
        self.database_name = config["REDIS_DATABASE"]