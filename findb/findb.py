from datetime import datetime
from os import path, remove
from six import iteritems
from six.moves.cPickle import dump, load, HIGHEST_PROTOCOL
from time import time

from .exceptions import DecrementNonInt, FileLoadError, FileWriteError, IncrementNonInt


class FinDB(object):
    """
    This is the basic object of FinDB. This is where the persistance will come
    from for now. We'll get to writing to disk, hopefully, later.
    """

    def __init__(self, location):
        self.last_saved = None
        self.location = location
        self.data = {}
        if self.location:
            self._load()

    def __iter__(self):
        return iteritems(self.data)

    def _load(self):
        """
        The `_load` function sees if the location of the database exists, and
        if so reads it into memory.
        """
        if self.location and path.exists(self.location):
            try:
                fs = open(self.location, "rb")
            except Exception as e:
                raise e
            try:
                data = load(fs)
                self.last_saved = data["last_saved"]
                self.data = data["data"]
            except Exception:
                fs.close()
                raise FileLoadError("The given file could not be loaded")
            fs.close()
        else:
            self.data = {}
            self._save()

    def _save(self):
        if self.location:
            try:
                fs = open(self.location, "wb")
            except Exception as e:
                raise e
            try:
                self.last_saved = time()
                dump(self.__dict__, fs, HIGHEST_PROTOCOL)
                fs.close()
            except Exception:
                raise FileWriteError("Could not write database to file.")
        else:
            self.last_saved = time()

    def get(self, key):
        """
        The `get` function accepts a key and returns the the value associated
        to that key if it exists. If the key does not exist, it returns False.
        """
        try:
            return self.data[key]
        except KeyError:
            return False

    def incr(self, key, incr=1):
        """
        The `incr` fuction increments the number stored at key by incr.
        """
        value = self.get(key)
        if not value:
            value = 0
        if type(value) is not int:
            raise IncrementNonInt("You are attempting to increase a value that is not stored as an int.")
        else:
            value += incr
            self.set(key, value)
        return value

    def decr(self, key, decr=1):
        """
        The `decr` fuction decrements the number stored at key by decr.
        """
        value = self.get(key)
        if not value:
            value = 0
        if type(value) is not int:
            raise DecrementNonInt("You are attempting to decrease a value that is not stored as an int.")
        else:
            value -= decr
            self.set(key, value)
        return value

    def lastsave(self):
        """
        The `lastsave` function returns the last time the database was saved.
        """
        return datetime.fromtimestamp(self.last_saved)

    def keys(self):
        """
        The `getall` function returns all the possible keys in the database.
        """
        return list(self.data.keys())

    def dbsize(self):
        """
        The `dbsize` function returns the number of keys in the database.
        """
        return len(self.data.keys())

    def set(self, key, value):
        """
        The `set` function accepts a key and value then sets that into the db.
        """
        self.data[key] = value
        self._save()
        return True

    def delete(self, key):
        """
        The `pop` function accepts a key and removes that key-value pair from
        the database.
        """
        self.data.pop(key)
        self._save()
        return True

    def flushdb(self):
        """
        The `drop` function will drop all key-values from the database.
        """
        self.data = {}
        self._save()
        return True

    def deletedb(self):
        if self.location:
            remove(self.location)
        else:
            self.flushdb()
