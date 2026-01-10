'В этом модуле описаны различные типы, датаклассы и перечисления Кардинала.'
from __future__ import annotations


from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Callable, Literal, Self
from enum import Enum
from abc import ABC, abstractmethod


__all__ = [
    'Plugin',
    'Handler',
    'Release',
    'CheckUpdatesResponse',
    'CardinalManager',
    'CheckUpdatesResponses',
    'InstallUpdateResponses'
]


# ---------------------------------------------------------------------------- #
#                                  Датаклассы                                  #
# ---------------------------------------------------------------------------- #
@dataclass
class Plugin:
    'Класс, описывающий плагин Кардинала.'
    uuid: str
    name: str
    version: str
    description: str
    credits: str
    dir: Path
    dependencies: dict
    raw_info: dict
    module: ModuleType | None = None
    handlers: dict[
        Literal[
            'PRE_INIT',
            'POST_INIT',
            'PRE_START',
            'POST_START',
            'PRE_STOP',
            'POST_STOP',
            'INIT_MESSAGE',
            'MESSAGES_LIST_CHANGED',
            'LAST_CHAT_MESSAGE_CHANGED',
            'NEW_MESSAGE',
            'INIT_ORDER',
            'NEW_ORDER',
            'ORDERS_LIST_CHANGED',
            'ORDER_STATUS_CHANGED',
            'PROFILE_UPDATE'
        ] | str,
        list[Handler]
    ] = field(default_factory=dict)


@dataclass
class Handler:
    'Класс, описывающий хендлер Кардинала.'
    plugin_uuid: str
    type: Literal[
        'PRE_INIT',
        'POST_INIT',
        'PRE_START',
        'POST_START',
        'PRE_STOP',
        'POST_STOP',
        'INIT_MESSAGE',
        'MESSAGES_LIST_CHANGED',
        'LAST_CHAT_MESSAGE_CHANGED',
        'NEW_MESSAGE',
        'INIT_ORDER',
        'NEW_ORDER',
        'ORDERS_LIST_CHANGED',
        'ORDER_STATUS_CHANGED',
        'PROFILE_UPDATE'
    ] | str
    priority: int
    func: Callable[..., None]


@dataclass
class Release:
    'Класс, описывающий релиз.'
    name: str
    description: str
    sources_link: str


@dataclass
class CheckUpdatesResponse:
    'Класс, описывающий ответ при проверке обновлений Кардинала.'
    response: CheckUpdatesResponses
    error: Exception | None = None
    releases: list[Release] | None = None


# ---------------------------------------------------------------------------- #
#                              Абстрактные классы                              #
# ---------------------------------------------------------------------------- #
class CardinalManager(ABC):
    '''
    Абстрактный класс CardinalManager'а
    '''
    instance: Self = None
    '''Экземпляр CardinalManager'а.'''


    def __new__(cls):
        if not cls.instance: cls.instance = super().__new__(cls)

        return cls.instance


    def __init__(self):
        if hasattr(self, '__initiated'): return

        self.__initiated = True


    @abstractmethod
    def get_actual_cardinal_package(self) -> ModuleType:
        '''
        Возвращает модуль Кардинала.

        **ВАЖНО!!! В этой функции должна быть описана логика импорта модуля с возможностью ре-импорта.**

        :return: Модуль Кардинала.
        :rtype: ModuleType
        '''
        ...


    @abstractmethod
    def start_cardinal(self, name: str, version: str) -> None:
        '''
        Инициализирует и запускает Кардинал.

        **ВАЖНО!!! Класс Кардинала должен быть получен из модуля, полученного через get_actual_cardinal_package().**

        :param name: Имя экземпляра.
        :type name: str
        :param version: Версия Кардинала.
        :type version: str
        '''
        ...


    @abstractmethod
    def stop_cardinal(self, name: str) -> None:
        '''
        Останавливает Кардинал.

        :param name: Имя экземпляра Кардинала.
        :type name: str
        '''
        ...


    @abstractmethod
    def restart_cardinal(self, cardinal_name: str):
        '''
        Останавливает Кардинал, ре-импортит пакеты, после чего повторно инициализирует и запускает Кардинал.

        **ВАЖНО!!! Класс Кардинала должен быть получен из модуля, полученного через get_actual_cardinal_package().**

        :param cardinal_name: Имя экземпляра Кардинала. 
        :type cardinal_name: str
        '''
        ...


    def update_cardinal(self, release: Release) -> None:
        '''
        Скачивает и устанавливает обновление Кардинала.

        :param release: Информация об обновлении.
        :type release: Release
        '''
        ...


    def create_cardinal_backup(self, name: str) -> None:
        'Создает бекап Кардинала (конфиги, кеш, плагины).'
        ...


# ---------------------------------------------------------------------------- #
#                             Перечисления (Enums)                             #
# ---------------------------------------------------------------------------- #
class CheckUpdatesResponses(Enum):
    'Ответы, возвращаемые при проверке обновлений Кардинала.'
    TAGS_NOT_FOUND = 'Не удалось получить список версий'
    CARDINAL_IS_UP_TO_DATE = 'Кардинал обновлен до последней версии'
    RELEASES_NOT_FOUND = 'Не удалось получить информацию о новой версии'
    UPDATE_AVAILABLE = 'Доступно обновление'


class InstallUpdateResponses(Enum):
    'Ответы, возвращаемые при установке обновления Кардинала.'
    UPDATE_FOLDER_NOT_FOUND = 'Папка с обновлением отсутствует'
    UNEXCEPTED_ERROR = 'Произошла непредвиденная ошибка'
    INSTALL_SUCCESS = 'Установка успешна'
    REBOOT_IS_REQUIRED = 'Установка успешна. Требуется полная перезагрузка программы'