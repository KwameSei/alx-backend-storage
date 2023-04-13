#!/usr/bin/env python3
""" Creating or writing string to Redis """
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """ Cache class that stores cached data """
    def __init__(self):
        """ Init method """
        # Creating an instance of the Redis client
        self._redis = redis.Redis()    # _redis is a private instance attribute
        # Clearing any existing data in the Redis instance
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Method tht stores data """
        # Generating a random key
        key = str(uuid4())
        # Storing the input data in Redis using the random key
        self._redis.set(key, data)
        return key
