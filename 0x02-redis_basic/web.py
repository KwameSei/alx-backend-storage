#!/usr/bin/env python3
""" Creating or writing string to Redis """
import requests
import redis
from functools import lru_cache
from functools import wraps

redis = redis.Redis()


@lru_cache(maxsize=128)
def get_page(url: str) -> str:
    """ Function that returns the HTML content of a particular URL"""
    response = requests.get(url)
    count_key = f"count:{url}"
    # Increment the count of times this URL was accessed
    # with an expiration time of 10 seconds.
    redis.incr(count_key, amount=1)
    redis.expire(count_key, time=10)
    return response.text

def count_calls(func):
    """ Method that counts how many times a function is called """
    @wraps(func)
    def wrapper(url, *args, **kwargs):
        count_key = f"count:{url}"
        # Increment the count of times this URL was accessed
        # with an expiration time of 10 seconds.
        redis.incr(count_key, amount=1)
        redis.expire(count_key, time=10)
        return func(url, *args, **kwargs)
    return wrapper

@count_calls
def get_page(url: str) -> str:
    """ Function that returns the HTML content of a particular URL"""
    response = requests.get(url)
    return response.text