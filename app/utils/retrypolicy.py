class RetryPolicy:
    def __init__(self, maxRetry: int, backoffInterval: int):
        self.maxRetry = maxRetry
        self.backoffInterval = backoffInterval

    def getMaxRetry(self):
        return self.maxRetry
    
    def getBackoffInterval(self):
        return self.backoffInterval