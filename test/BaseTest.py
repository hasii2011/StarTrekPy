
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
        with open(BaseTest.JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

