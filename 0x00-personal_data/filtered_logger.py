#!/usr/bin/env python3
'''function to return log message obfuscated'''
import re
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
from typing import List
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''initialize class with fields'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''filter information in log records'''
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    '''function returns log message'''
    pattern = "({})=[^{}]+".format('|'.join(fields), separator)
    return re.sub(
            pattern, lambda m: '{}={}'.format(m.group(1), redaction), message)


def get_logger() -> logging.Logger:
    '''Create and Configure a logger for user data'''
    # create and configure logger
    logger = logging.getLoger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Sream handler with the RedactingFormatter
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # add handler to the logger
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    '''Creates a connection to database using environmetal variables'''
    # get environment variables
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD'. '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # check if database name is provided
    if db_name is None:
        raise ValueError('Environment var PERSONAL_DATA_DB_NAME must be set')

    # connection
    connection = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
            )
    return connection
