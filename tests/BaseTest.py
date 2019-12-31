
from os import path as osPath
from os import chdir as osChangeDirectory

import json

import logging.config

import logging
import logging.config

from unittest import TestCase


class BaseTest(TestCase):
    """"""

    JSON_LOGGING_CONFIG_FILENAME = 'unitTestLoggingConfiguration.json'

    @classmethod
    def setUpLogging(cls):
        """"""
        loggingConfigFilename: str = cls.findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls) -> str:
        """"""
        upDir = f'tests/{BaseTest.JSON_LOGGING_CONFIG_FILENAME}'
        if osPath.isfile(upDir):
            return upDir

        if osPath.isfile(BaseTest.JSON_LOGGING_CONFIG_FILENAME):
            return BaseTest.JSON_LOGGING_CONFIG_FILENAME
        else:
            osChangeDirectory("../")
            return cls.findLoggingConfig()
