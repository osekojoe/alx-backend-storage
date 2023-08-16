#!/usr/bin/env python3
'''
Create a Cache class. In the __init__ method, store an instance of the Redis
  client as a private variable named _redis (using redis.Redis()) and flush
  the instance using flushdb.
Create a store method that takes a data argument and returns a string.
 The method should generate a random key (e.g. using uuid), store the input
  data in Redis using the random key and return the key.
Type-annotate store correctly. Remember that data can be a str, bytes, int
  or float.
'''


import redis
import uuid
from functools import wraps
from typing import Union, Callable
from redis.client import Redis


type_union = Union[str, bytes, int, float, None]


def count_calls(method: Callable) -> Callable:
    '''count how many times methods of the Cache class are called'''
    # key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''wrapper method - replace the original method when it's
        decorated'''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        '''store an instance of the Redis client as a private variable
           and flush the instance
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]):
        '''Create a store method that takes a data argument and returns
        a string'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> type_union:
        '''convert the data back to the desired format'''
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        '''automatically parametrize Cache.get with the correct conversion
        function.'''
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        '''automatically parametrize Cache.get with the correct conversion
        function.'''
        return self.get(key, fn=int)
