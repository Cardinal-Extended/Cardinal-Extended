
from dynaconf import Dynaconf
from dynaconf import loaders as DynaLoaders
from dynaconf.utils.boxing import DynaBox


from pathlib import Path
from typing import Any
import tomllib


__all__ = [
    'Config',
    'configs_dir',
    'settings_path',
    'logger_config_path',
]


configs_dir = Path(__file__).parent
settings_path = configs_dir / 'settings.toml'
default_settings_path = configs_dir / 'default_settings.toml'
logger_config_path = configs_dir / 'logger_config.toml'


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
        except: return self.config.get(name)


    def __get_config(
            self,
            section: str | None = None
    ) -> Dynaconf:
        return Dynaconf(
            settings_files=[settings_path],
            environments=True if section else False,
            env=section
        )


    @staticmethod
    def default() -> dict[str, Any]:
        'Стандартные настройки.'
        with open(default_settings_path, 'rb') as fp: data = tomllib.load(fp)

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
                if settings_path.exists():
                    with open(settings_path, 'rb') as fp: data = tomllib.load(fp)
                else: data = {}

                data[self.__section] = to_save

            else: data = to_save

            DynaLoaders.write(str(settings_path), data)

        else:
            data = DynaBox(self.config) if isinstance(self.config, dict) else DynaBox(self.config.to_dict()).to_dict()

            DynaLoaders.write(
                str(settings_path),
                data,
                self.__section,
                True if self.__section else False
            )

        return