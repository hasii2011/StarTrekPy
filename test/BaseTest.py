
import os

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
        cls.findLoggingConfig()
        with open(BaseTest.JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls):
        """"""
        if os.path.isfile(BaseTest.JSON_LOGGING_CONFIG_FILENAME):
            return
        else:
            os.chdir("../")
            cls.findLoggingConfig()
