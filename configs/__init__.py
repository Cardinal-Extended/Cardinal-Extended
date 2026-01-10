
from dynaconf import Dynaconf
from dynaconf import loaders as DynaLoaders
from dynaconf.utils.boxing import DynaBox


from pathlib import Path
from typing import Any
import tomllib


__all__ = [
    'Config',
    'CONFIGS_DIR',
    'SETTINGS_PATH',
    'LOGGER_CONFIG_PATH',
]


CONFIGS_DIR = Path(__file__).parent
SETTINGS_PATH = CONFIGS_DIR / 'settings.toml'
DEFAULT_SETTINGS_PATH = CONFIGS_DIR / 'default_settings.toml'
LOGGER_CONFIG_PATH = CONFIGS_DIR / 'logger_config.toml'


class Config:
    def __init__(
            self,
            section: str | None = None
    ):
        '''
        Класс настроек.

        :param section: Секция настроек, defaults to None.
        :type section: str | None, optional
        '''
        self.__section = section


        self.config = self.__get_config(section)
        'Настройки.'


    def __getattribute__(self, name):
        try: return super().__getattribute__(name)
        except: return self.config[name]


    def __get_config(
            self,
            section: str | None = None
    ) -> Dynaconf:
        return Dynaconf(
            settings_files=[SETTINGS_PATH],
            environments=True if section else False,
            env=section
        )


    @staticmethod
    def default() -> dict[str, Any]:
        'Стандартные настройки.'
        with open(DEFAULT_SETTINGS_PATH, 'rb') as fp: data = tomllib.load(fp)

        return data


    def set_default(self) -> None:
        'Устанавливает стандартные настройки.'
        config = self if not self.__section else Config()
        config.config = config.default()
        config.save(True)


        self.config = self.__get_config(self.__section)

        return


    def save(self, force_save: bool = False) -> None:
        'Сохраняет текущие настройки в файле.'
        if force_save:
            to_save = DynaBox(self.config) if isinstance(self.config, dict) else DynaBox(self.config.to_dict()).to_dict()

            if self.__section:
                if SETTINGS_PATH.exists():
                    with open(SETTINGS_PATH, 'rb') as fp: data = tomllib.load(fp)
                else: data = {}

                data[self.__section] = to_save

            else: data = to_save

            DynaLoaders.write(str(SETTINGS_PATH), data)

        else:
            data = DynaBox(self.config) if isinstance(self.config, dict) else DynaBox(self.config.to_dict()).to_dict()

            DynaLoaders.write(
                str(SETTINGS_PATH),
                data,
                self.__section,
                True if self.__section else False
            )

        return