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
        """ Method the stores data """
        # Generating a random key
        key = str(uuid4())
        # Storing the input data in Redis using the random key
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: callable = None) -> \
            Union[str, bytes, int, float]:
        """ Method that gets data in any format """
        # Retrieving the data stored in Redis using the key
        data = self._redis.get(key)
        # Apply fn to the data if it exists
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Method that gets data as a string """
        # Retrieving the data stored in Redis using the key
        data = self._redis.get(key)
        # Converting the data to a string
        return data.decode('utf-8')

    def get_int(self, key: str) -> int:
        """ Method that gets data as an integer """
        # Retrieving the data stored in Redis using the key
        data = self._redis.get(key)
        # Converting the data to an integer
        return int.from_bytes(data, 'big')
