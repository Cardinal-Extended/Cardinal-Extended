
from pathlib import Path


# ---------------------------------------------------------------------------- #
#                               Пути и директории                              #
# ---------------------------------------------------------------------------- #
HOME_DIR = Path(__file__).parent.parent
'Путь к папке Кардинала.'

CONFIGS_DIR = HOME_DIR / 'configs'
'Путь к папке с конфигами.'

LOGGER_CONFIG_PATH = CONFIGS_DIR / 'logger_config.toml'
'Путь к конфигу логгера.'

LOGS_DIR = HOME_DIR / 'logs'
'Путь к папке с логами.'

PATHS_CONFIG_PATH = CONFIGS_DIR / 'paths.toml'
'Путь к конфигу кастомных путей Кардинала.'

VERSION_PATH = HOME_DIR / 'VERSION'
'Путь к версии Кардинала.'


from .config import *


# ------------------------ Кастомные пути и директории ----------------------- #
__paths_config = _Config('PATHS')

for __config_path_name in __paths_config.config: globals()[__config_path_name] = HOME_DIR.joinpath(str(__paths_config.config[__config_path_name]))


__all__ = [
    'HOME_DIR',
    'CONFIGS_DIR',
    'LOGGER_CONFIG_PATH',
    'PATHS_CONFIG_PATH',
    'VERSION_PATH',
    '_Config',
    'SETTINGS_PATH',
]


SETTINGS_PATH = CONFIGS_DIR / 'settings.toml'
DEFAULT_SETTINGS_PATH = CONFIGS_DIR / 'default_settings.toml'