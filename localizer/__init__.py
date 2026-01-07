from pathlib import Path

LOCALES_DIR = Path(__file__).parent / 'locales'


import re

ARG_PATTERN = re.compile(r'\{\}')
KWARG_PATTERN = re.compile(r'\{\w+\}')


from . import exceptions


from .localizer import *


__all__ = [
    'Localizer',
    'LOCALES_DIR',
    'exceptions'
]