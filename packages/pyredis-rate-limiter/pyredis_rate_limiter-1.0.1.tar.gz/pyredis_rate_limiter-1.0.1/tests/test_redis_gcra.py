# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from pyredis_rate_limiter import Limiter, RedisClient, Result, per_second


class RedisGCRATestCase(unittest.TestCase):

    def setUp(self):
        self.redis_client = RedisClient(client_conf={
            "endpoint": "localhost:6379",
            "password": "sOmE_sEcUrE_pAsS",
            "db": 1,
            "socket_timeout": 0.5,
            "socket_connect_timeout": 0.25
        })
        connected = self.redis_client.is_connected()
        if connected:
            print("Redis connection established.")
            self.rl = Limiter(redis_conn=self.redis_client.get_connection(), async_mode=False)
        else:
            print("Redis connection failed.")
            self.rl = None
    
    def test_allow(self):
        if self.rl is None:
            self.skipTest("Redis connection failed.")
        key = "test_redis_gcra"
        limit = per_second(5)
        for _ in range(10):
            print(f"Invoke allow(key={key}, limit={limit})")
            result, error = self.rl.allow(key, limit)
            self.assertIsNone(error)
            self.assertIsInstance(result, Result)
            print(f"Result: {result}")

    def tearDown(self):
        if self.rl is not None:
            self.redis_client.close()


if __name__ == "__main__":
    unittest.main()
