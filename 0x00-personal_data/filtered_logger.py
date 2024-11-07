#!/usr/bin/env python3
'''function to return log message obfuscated'''
import re
from typing import List
import logging


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
