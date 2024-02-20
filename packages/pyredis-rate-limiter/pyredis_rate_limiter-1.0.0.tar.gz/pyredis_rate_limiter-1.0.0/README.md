This is an implementation of [GCRA](https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm) for rate limiting based on Redis.

The code requires Redis version 3.2 or newer since it relies on [replicate_commands](https://redis.io/commands/eval/#replicating-commands-instead-of-scripts) feature.

### How to Install?

```shell
pip install pyredis_rate_limiter
```

### How to Use?

Here is a short example.
```python
# -*- coding: utf-8 -*-
import asyncio
from typing import Optional

import redis as aio_redis
from loguru import logger as loguru_logger
from pyredis_rate_limiter import (
    Limit,
    Limiter,
    per_second
)

_rl_instance: Optional[Limiter] = None


def init_rl_instance(redis_conn: aio_redis.Redis):
    global _rl_instance
    _rl_instance = Limiter(redis_conn)


def rl_instance() -> Limiter:
    return _rl_instance


async def take_token(key: str, limit: Limit, block_wait: bool = False) -> Optional[int]:
    token: Optional[int] = None

    ret, _ = await rl_instance().aio_allow(key, limit)
    if ret is None:
        return token
    if ret.allowed == 0:
        if block_wait:
            wait_until_available = ret.retry_after_in_sec
            loguru_logger.warning(f"Token for key:{key} exceeds, wait {wait_until_available} secs until resource turns to be available")
            await asyncio.sleep(ret.retry_after_in_sec)
        else:
            loguru_logger.error(f"no token available for key:{key}")
    else:
        token = 1
    return token


async def send_sm():
    token = await take_token(key="send_sm_handler", limit=per_second(5))
    if token is None:
        # do sth
    else:
        # do sth
```
