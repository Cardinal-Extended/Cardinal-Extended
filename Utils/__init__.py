from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent / 'plugins'
LOGS_DIR = Path(__file__).parent.parent / 'logs'


import re

ENTITY_RE = re.compile(r'\$photo=\d+|\$new|(\$sleep=(\d+\.\d+|\d+))')
'Шаблон элемента (сущности) сообщения.'

CLEAR_RE = re.compile(r'(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))|(\n)|(\r)')


from . import exceptions


from .types import *
from .logger import *
from .cardinal_tools import *


__all__ = [
    'PLUGIN_DIR',
    'LOGS_DIR',
    'ENTITY_RE',
    'exceptions',
    'Plugin',
    'Handler',
    'ColoredFormatter',
    'FileFormatter',
    'check_proxy',
    'set_console_title'
]