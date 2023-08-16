#!/usr/bin/env python3
'''
uses the requests module to obtain the HTML content of a particular URL
  and returns it.
track how many times a particular URL was accessed in the key "count:{url}"
  and cache the result with an expiration time of 10 seconds.
'''


import requests
import redis
from functools import wraps
from typing import Callable
from redis.client import Redis


def cache_page(method: Callable) -> Callable:
    ''''''
    @wraps(method)
    def wrapper(self, url: str) -> str:
        ''''''
        cached = self._redis.get(url)
        if cached is not None:
            return cached.decode("utf-8")

        html = method(self, url)

        self._redis.setex(url, 10, html)
        return html
    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()

    @cache_page
    def get_page(self, url: str) -> str:
        '''uses the requests module to obtain the HTML content of
        a particular URL and returns it.'''
        response = requests.get(url)
        return response.text


cache = Cache()
url = "http://slowwly.robertomurray.co.uk"

html = cache.get_page(url)
print(html)
