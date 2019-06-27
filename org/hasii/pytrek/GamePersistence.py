
import logging


class SaveGame(object):
    """"""

    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton               = object.__new__(SaveGame)
            cls._singleton.__initialized = False
        return cls._singleton

    def __init__(self):
        """"""

        if self.__initialized is True:
            return
        else:
            self.__initialized = True

        self.logger = logging.getLogger(__name__)

    def save(self):
        """"""

    def load(self):
        """"""
