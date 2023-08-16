#!/usr/bin/env python3
'''
uses the requests module to obtain the HTML content of a particular URL
  and returns it.
track how many times a particular URL was accessed in the key "count:{url}"
  and cache the result with an expiration time of 10 seconds.
'''


import redis
import requests
from typing import Callable
from functools import wraps

redis = redis.Redis()


def cache_page(fn: Callable) -> Callable:
    """ Decorator wrapper """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorator guy """
        redis.incr(f"count:{url}")
        cached_content = redis.get(f"cached:{url}")
        
        if cached_content:
            return cached_content.decode('utf-8')
        
        html = fn(url)
        redis.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@cache_page
def get_page(url: str) -> str:
    '''uses the requests module to obtain the HTML content of
    a particular URL and returns it.'''
    response = requests.get(url)
    return response.text
