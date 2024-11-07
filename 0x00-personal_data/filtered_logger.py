#!/usr/bin/env python3
'''function to return log message obfuscated'''
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    '''function returns log message'''
    pattern = "({})=[^{}]+".format('|'.join(fields), separator)
    return re.sub(
            pattern, lambda m: '{}={}'.format(m.group(1), redaction), message)
