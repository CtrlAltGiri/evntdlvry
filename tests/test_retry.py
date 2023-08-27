import unittest
from utils.retry import Retry
from utils.retrypolicy import RetryPolicy

class TestRetry(unittest.TestCase):

    def test_constructor(self):
        rp = RetryPolicy(1, 1)
        r = Retry(rp)
        self.assertIsNotNone(r)
        self.assertEqual(1, r.retrypolicy.getMaxRetry())
        self.assertEqual(1, r.retrypolicy.getBackoffInterval())

    def test_retry(self):
        rp = RetryPolicy(1, 1)
        r = Retry(rp)
        r.run(lambda x: x < 1,lambda: 0, lambda x: 0, lambda: 0)

if __name__ == '__main__':
    unittest.main()
