import redis
from enum import Enum
from abc import ABC, abstractmethod

class DB(ABC):
    @abstractmethod
    def push(self, message, messageId):
        pass

    @abstractmethod
    def pop(self, messageId):
        pass

    @abstractmethod
    def getMessageId(self, queue):
        pass

class TestDB(DB):
    def push(self, message, messageId):
        pass

    def pop(self, messageId):
        pass

    def getMessageId(self, queue):
        pass

class RedisQueue(DB):
    def setup_redis(self, config):
        self.db = redis.Redis(
            host=config["REDIS_HOST"],
            port=config["REDIS_PORT"],
            db=config["REDIS_DBNUMBER"],
            password=config["REDIS_PSWRD"],
            decode_responses=True,
        )

        self.db.ping()
        self.consumers = [
            'http://consumer1:5000/consumeEvent', 
            'http://consumer2:5000/consumeEvent', 
            'http://consumer3:5000/consumeEvent']

    def push(self, message, messageId):
        self.db.set(messageId, message)
        for consumer in self.consumers:
            self.db.lpush(consumer, messageId)

    def pop(self):
        return self.db.lpop(self.database_name)

    def getMessageId(self, queueName):
        incrName = queueName + ".nextIndex"
        return self.db.incr(incrName)

    def __init__(self, config):
        self.setup_redis(config)
        self.database_name = config["REDIS_DATABASE"]

class DBType(Enum):
    TEST = 1
    REDIS = 2

class DBFactory:
    def __init__(self, type):
        self.type = type
    
    def getInstance(self, config) -> DB:
        if self.type == DBType.TEST:
            return TestDB()
        else:
            return RedisQueue(config)