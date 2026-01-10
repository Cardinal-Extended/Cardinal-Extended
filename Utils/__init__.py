
GITHUB_TAGS_URL = 'https://api.github.com/repos/Shiro-Okamoto/CardinalExtended/tags'
GITHUB_RELEASES_URL = 'https://api.github.com/repos/Shiro-Okamoto/CardinalExtended/releases'


from pathlib import Path

HOME_DIR = Path(__file__).parent.parent

# TODO Move all paths to config
PLUGIN_DIR = HOME_DIR / 'plugins'

LOGS_DIR = HOME_DIR / 'logs'

STORAGE_DIR = HOME_DIR / 'storage'
CACHE_DIR = STORAGE_DIR / 'cache'
UPDATE_DIR = CACHE_DIR / 'update'
BACKUP_DIR = CACHE_DIR/ 'backup'

VERSION_PATH = HOME_DIR / 'VERSION'

with open(VERSION_PATH, 'r', encoding='utf-8') as fp: VERSION = fp.read()


import re

ENTITY_RE = re.compile(r'\$photo=\d+|\$new|(\$sleep=(\d+\.\d+|\d+))')
'Шаблон элемента (сущности) сообщения.'

CLEAR_RE = re.compile(r'(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))|(\n)|(\r)')


from . import exceptions


from .types import *
from .logger import *
from .cardinal_tools import *
from .updates import *


__all__ = [
    'HOME_DIR',
    'PLUGIN_DIR',
    'LOGS_DIR',
    'STORAGE_DIR',
    'CACHE_DIR',
    'UPDATE_DIR',
    'BACKUP_DIR',
    'VERSION_PATH',
    'VERSION',
    'ENTITY_RE',
    'exceptions',
    'Plugin',
    'Handler',
    'Release',
    'CheckUpdatesResponse',
    'CardinalManager',
    'CheckUpdatesResponses',
    'InstallUpdateResponses',
    'ColoredFormatter',
    'FileFormatter',
    'check_proxy',
    'set_console_title',
    'get_new_releases',
    'download_zip',
    'extract_update_archive',
    'create_backup',
    'extract_backup_archive',
    'install_release',
    'install_backup'
]