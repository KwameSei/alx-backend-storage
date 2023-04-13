#!/usr/bin/env python3
""" Creating or writing string to Redis """
import redis
from uuid import uuid4
from typing import Union
import functools
import json


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

    def count_calls(self, f: callable) -> callable:
        """ Method that counts how many times a function is called """
        # Generating a random key
        key = str(uuid4())
        # Storing the input data in Redis using the random key
        self._redis.set(key, 0)

        # Creating a wrapper function
        def wrapper(*args, **kwargs):
            """ Wrapper function """
            # Incrementing the counter
            self._redis.incr(key)
            # Calling the original function
            return f(*args, **kwargs)
        # Returning the wrapper function
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Method the stores data """
        # Generating a random key
        key = str(uuid4())
        # Storing the input data in Redis using the random key
        self._redis.set(key, data)
        return key

    def call_history(method):
        """ Method that stores the history of inputs and outputs for a
            particular function """
        # Creating a wrapper function
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            """ Wrapper function """
            input_data = method.__qualname__ + ":inputs"
            output_data = method.__qualname__ + ":outputs"
            # Storing the input data in Redis using the random key
            self._redis.rpush(input_data, json.dumps(args))

            # Storing the output data in Redis using the random key
            output = method(self, *args, **kwargs)
            self._redis.rpush(output_data, json.dumps(output))

            return output
        # Returning the wrapper function
        return wrapper

    def replay(method, cache):
        """ Method that displays the history of calls of a particular
            function """
        input_data = method.__qualname__ + ":inputs"
        output_data = method.__qualname__ + ":outputs"

        inputs = cache._redis.lrange(input_data, 0, -1)
        outputs = cache._redis.lrange(output_data, 0, -1)
        number_of_calls = len(inputs)

        print("{} was called {} times:".format(method.__qualname__,
                                               number_of_calls))
        for i, (in_data, out_data) in enumerate(zip(inputs, outputs)):
            input_args = tuple(json.loads(in_data.decode('utf-8')))
            output_args = json.loads(out_data.decode('utf-8'))
            print("{}: {}(*{}) -> {}".format(i, method.__qualname__,
                                             input_args, output_args))
