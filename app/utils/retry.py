from .retrypolicy import RetryPolicy
import time

class Retry:
    def __init__(self, retrypolicy: RetryPolicy):
        self.retrypolicy = retrypolicy

    def run(self, conditionLambda, preprocess, funcToRun, cleanupLamda):
        maxRetry = self.retrypolicy.getMaxRetry()
        backoffInterval = self.retrypolicy.getBackoffInterval()

        try:
            preprocess()    
        except Exception as e:
            print("Exception from preprocess: ", e)

        timesComplete = 0
        while conditionLambda(timesComplete):
            failures = 0
            while failures < maxRetry:
                try:
                    funcToRun(failures != 0)
                    break
                except Exception as e:
                    failures += 1
                    sleepTime = pow(backoffInterval, failures)
                    print("sleeping for ", sleepTime, " seconds")
                    time.sleep(sleepTime)

            try:
                if failures >= maxRetry:
                    cleanupLamda()
            except Exception as e:
                print("Really fatal")
            
            timesComplete += 1