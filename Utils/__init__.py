'В данном модуле описаны различные типы, классы, методы, исключения и инструменты Кардинала.'
import re

ENTITY_RE = re.compile(r'\$photo=\d+|\$new|(\$sleep=(\d+\.\d+|\d+))')
'Шаблон элемента (сущности) сообщения.'


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
    'Tag',
    'Release',
    'CardinalWorker',
    'ColoredFormatter',
    'FileFormatter',
    'check_proxy',
    'set_console_title',
    'get_current_cardinal_version',
    'get_tags',
    'get_next_tag',
    'get_releases',
    'get_new_releases',
    'download_release',
    'extract_release',
    'install_release',
    'create_backup',
    'extract_backup_archive',
    'install_backup',
    'download_zip',
    'extract_archive',
    'zipdir'
]