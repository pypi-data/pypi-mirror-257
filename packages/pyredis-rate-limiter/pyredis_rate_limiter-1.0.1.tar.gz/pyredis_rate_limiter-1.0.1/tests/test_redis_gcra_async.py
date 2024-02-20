# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from pyredis_rate_limiter import AioRedisClient, Limiter, Result, per_second


class RedisGCRATestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.redis_client = AioRedisClient(client_conf={
            "endpoint": "localhost:6379",
            "password": "sOmE_sEcUrE_pAsS",
            "db": 0,
            "socket_timeout": 0.5,
            "socket_connect_timeout": 0.25
        })
        connected = await self.redis_client.is_connected()
        if connected:
            print("\nRedis connection established.")
            self.rl = Limiter(redis_conn=self.redis_client.get_connection(), async_mode=False)
        else:
            print("Redis connection failed.")
            self.rl = None
    
    async def test_allow(self):
        if self.rl is None:
            self.skipTest("Redis connection failed.")
        key = "test_redis_gcra"
        limit = per_second(5)
        for _ in range(10):
            print(f"Invoke allow(key={key}, limit={limit})")
            result, error = await self.rl.aio_allow(key, limit)
            self.assertIsNone(error)
            self.assertIsInstance(result, Result)
            print(f"Result: {result}")

    async def asyncTearDown(self):
        if self.rl is not None:
            await self.redis_client.close()


if __name__ == "__main__":
    unittest.main()
