
GITHUB_TAGS_URL = 'https://api.github.com/repos/Shiro-Okamoto/CardinalExtended/tags'
GITHUB_RELEASES_URL = 'https://api.github.com/repos/Shiro-Okamoto/CardinalExtended/releases'


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