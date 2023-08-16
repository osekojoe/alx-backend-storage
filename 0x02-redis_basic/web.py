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
    '''Decorator wrapper'''

    @wraps(method)
    def wrapper(url):
        '''wrapper'''
        redis.incr(f"count:{url}")
        cached_content = redis.get(f"cached:{url}")
        if cached_content is not None:
            return cached_content.decode("utf-8")

        html_content = method(url)

        redis.setex(f"cached:{url}", 10, html_content)
        return html
    return wrapper


@cache_page
def get_page(url: str) -> str:
    '''uses the requests module to obtain the HTML content of
    a particular URL and returns it.'''
    response = requests.get(url)
    return response.text
