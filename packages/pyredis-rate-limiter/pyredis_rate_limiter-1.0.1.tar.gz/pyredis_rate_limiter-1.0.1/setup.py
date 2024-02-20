# -*- coding: utf-8 -*-
import os

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from setuptools import find_packages, setup

README = '''
This is an implementation of [GCRA](https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm) for rate limiting based on Redis.

The code requires Redis version 3.2 or newer since it relies on [replicate_commands](https://redis.io/commands/eval/#replicating-commands-instead-of-scripts) feature.

### How to Install?

```shell
pip install pyredis-rate-limiter
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
'''

setup(
    name='pyredis_rate_limiter',
    version='1.0.1',
    description='A Redis-backed rate limiting based on GCRA implementation in Python',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Adam Zhou',
    author_email='adamzhouisnothing@gmail.com',
    url='https://github.com/amazingchow/redlock-py',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jsonschema==4.21.1",
        "loguru==0.7.2",
        "redis==5.0.1"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': []
    }
)
