
class EventEngine:

    _singleton: 'EventEngine' = None

    def __new__(cls, *args, **kwargs):

        if not cls._singleton:
            cls._singleton = object.__new__(EventEngine)
            cls._singleton.__initialized = False
        return cls._singleton

    def __init__(self):

        if self.__initialized is True:
            return
        else:
            self.__initialized = True
