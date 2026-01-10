'Здесь описан управляющий Кардиналом класс.'
from __future__ import annotations


from Utils import (
    CardinalManager as CardinalManagerABC, Release, create_backup, create_backup, download_zip, extract_update_archive, install_release, InstallUpdateResponses
)

import importlib.util


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cardinal import Cardinal
    from typing import NoReturn


import logging
from pathlib import Path
from time import sleep
from threading import Thread
from types import ModuleType


__all__ = [
    'CardinalManager'
]


log = logging.getLogger('CardinalManager')


CARDINAL_PATH = Path(__file__).parent / 'cardinal.py'


class CardinalManager(CardinalManagerABC):
    'Класс, управляющий процессом Кардинала.'
    def __new__(cls): return super().__new__(cls)


    def __init__(self):
        super().__init__()

        if hasattr(self, '__initiated'): return


        self.cardinals: dict[str, Cardinal] = {}
        'Список управляемых Кардиналов.'


    def get_cardinal(self, name: str) -> Cardinal | None:
        '''
        Возвращает экземпляр Кардинала.

        :param name: Имя экземпляра.
        :type name: str
        :return: Экземпляр Кардинала, если он существует.
        :rtype: Cardinal | None
        '''

        return self.cardinals.get(name)


    def __import_cardinal(self) -> None:
        log.debug(f'Importing Cardinal package.')

        self.cardinal_package_spec = importlib.util.spec_from_file_location(CARDINAL_PATH.stem, CARDINAL_PATH)

        self.cardinal_package = importlib.util.module_from_spec(self.cardinal_package_spec)

        self.cardinal_package_spec.loader.exec_module(self.cardinal_package)

        return


    def get_actual_cardinal_package(self) -> ModuleType:
        'Возвращает модуль Кардинала.'
        log.info(f'Getting an actual Cardinal package.')

        self.__import_cardinal()


        return self.cardinal_package


    def start_cardinal(self, name: str, version: str) -> None:
        '''
        Инициализирует и запускает Кардинал.

        :param name: Имя экземпляра.
        :type name: str
        :param version: Версия Кардинала.
        :type version: str
        '''
        log.info(f'Starting Cardinal.')

        if self.get_cardinal(name): raise ValueError('Кардинал уже инициализирован!')


        cardinal: Cardinal = self.get_actual_cardinal_package().Cardinal(name, version)

        self.cardinals[name] = cardinal


        self.cardinals[name].init()


        cardinal.cardinal_manager = self

        self.cardinal_running_thread = Thread(target=cardinal.start, daemon=True)
        self.cardinal_running_thread.start()


    def stop_cardinal(self, name: str):
        'Останавливает Кардинал. Удаляет пакеты и Кардинал из кеша.'
        self.cardinals[name].stop()


        del self.cardinal_package.Cardinal.instances[name]

        del self.cardinals[name]

        del self.cardinal_package
        del self.cardinal_package_spec


    def restart_cardinal(self, name: str):
        'Останавливает Кардинал, ре-импортит пакеты, после чего перезапускает Кардинал.'
        cardinal = self.get_cardinal(name)
        version = cardinal.version

        self.stop_cardinal(name)

        self.start_cardinal(name, version)


    def update_cardinal(self, release: Release) -> None:
        '''
        Скачивает и устанавливает обновление Кардинала.

        :param release: Информация об обновлении.
        :type release: Release
        '''
        log.info('Updating Cardinal.')

        download_zip(release.sources_link)


        release_folder = extract_update_archive()

        result = install_release(release_folder)


        if result in [InstallUpdateResponses.UPDATE_FOLDER_NOT_FOUND, InstallUpdateResponses.UNEXCEPTED_ERROR]: raise Exception(result.value)


        if result is InstallUpdateResponses.REBOOT_IS_REQUIRED: log.info(f'Cardinal updated successfully, but reboot is required.')

        return


    def create_cardinal_backup(self, name: str) -> None:
        '''
        Создает бекап Кардинала (конфиги, кеш, плагины).

        :param name: Имя экземпляра.
        :type name: str
        :raises exceptions.CreateBackupError: Если не удалось создать бекап.
        '''
        log.info('Creating Cardinal backup.')

        create_backup()


        return


    def loop(self) -> NoReturn:
        'Бесконечный цикл. Ничего не делает.'
        while True: sleep(600)