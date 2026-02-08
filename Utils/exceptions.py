'В данном модуле описаны все кастомные исключения Кардинала.'
from __future__ import annotations


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Plugin, Tag, Release

    from pathlib import Path
    from requests import Response


# ---------------------------------------------------------------------------- #
#                                    Прокси                                    #
# ---------------------------------------------------------------------------- #
class ProxyCheckError(Exception):
    def __init__(self, proxies: dict[str, str]):
        '''
        Исключение, поднимающееся при неудачной попытке проверки прокси.

        :param proxies: Прокси.
        :type proxies: dict[str, str]
        '''
        self.proxies = proxies


    def __str__(self): return f'Ошибка при проверке прокси {self.proxies}'


# ---------------------------------------------------------------------------- #
#                              Ошибки при запросах                             #
# ---------------------------------------------------------------------------- #
class GetBalanceError(Exception):
    def __init__(self):
        '''
        Исключение, поднимающееся при неудачной попытке получения баланса аккаунта.
        '''


    def __str__(self): return 'Не удалось получить баланс'


class ProfileUpdateError(Exception):
    def __init__(self):
        '''
        Исключение, поднимающееся при неудачной попытке обновления профиля.
        '''


    def __str__(self): return 'Не удалось обновить профиль'


# ---------------------------------------------------------------------------- #
#                                    Плагины                                   #
# ---------------------------------------------------------------------------- #
class ModuleImportError(Exception):
    def __init__(self, module_path: Path):
        '''
        Исключение, поднимающееся при неудачной попытке загрузки модуля.

        :param module_path: Путь к модулю.
        :type module_path: Path
        '''
        self.module_path = module_path


    def __str__(self): return f'Ошибка при загрузке модуля {self.module_path.stem} ({self.module_path})'


class PluginNotTrustedException(Exception):
    def __init__(self, plugin: Plugin):
        '''
        Исключение, поднимающееся, если плагин отсутствует в доверенных.

        :param plugin: Объект плагина.
        :type plugin: Plugin
        '''
        self.plugin = plugin

    def __str__(self): return f'Плагин {self.plugin.name} {self.plugin.uuid} отсутствует в списке доверенных плагинов.'


class PluginDependenciesNotLoadedError(Exception):
    def __init__(self, plugin: Plugin, dependencies: dict[str]):
        '''
        Исключение, поднимающееся, если не загружены все зависимости плагина.

        :param plugin: Объект плагина.
        :type plugin: Plugin
        :param dependencies: Зависимости плагина.
        :type dependencies: dict[str]
        '''
        self.plugin = plugin
        self.dependencies = dependencies

    def __str__(self): return f'Загружены не все зависимости плагина {self.plugin.name} {self.plugin.uuid}: {[*self.dependencies]}'


# ---------------------------------------------------------------------------- #
#                                 Прочие ошибки                                #
# ---------------------------------------------------------------------------- #
class CardinalNotInitializedError(Exception):
    def __init__(self):
        '''
        Исключение, поднимающееся, если Кардинал не был инициализирован перед запуском.
        '''

    def __str__(self): return 'Кардинал должен быть инициализирован перед запуском!'


class CardinalWorkerRunningError(Exception):
    def __init__(self):
        '''
        Исключение, поднимающееся, если бесконечный цикл рабочего класса уже запущен.
        '''

    def __str__(self): return 'Бесконечный цикл уже запущен!'


class GitHubAPIUrlNotSpecified(Exception):
    def __init__(self):
        '''
        Исключение, поднимающееся, если отсутствует ссылка на репозиторий с обновлениями.
        '''

    def __str__(self): return 'Отсутствует ссылка на страницу GitHub для проверки обновлений'
    

# ---------------------------------------------------------------------------- #
#                                    Updater                                   #
# ---------------------------------------------------------------------------- #
class GitHubRequestError(Exception):
    def __init__(self, response: Response):
        '''
        Исключение, поднимающееся, если при запросе к репозиторию GitHub возникла ошибка.

        :param response: Ответ запроса.
        :type response: Response
        '''
        self.response = response


    def __str__(self): return f'Ошибка при запросе к GitHub {self.response.url} (Код ответа: {self.response.status_code})'


class GetNextTagError(Exception):
    def __init__(self, tag: str, tags: list[Tag]):
        '''
        Исключение, поднимающееся при ошибке получения следующего после tag тега.

        :param tag: Тег.
        :type tag: str
        :param tags: Список тегов.
        :type tags: list[Tag]
        '''
        self.tag = tag
        self.tags = tags


    def __str__(self): return f'Не удалось получить следующий тег после {self.tag}'


class ReleaseNotFoundError(Exception):
    def __init__(self, tag: Tag, releases: list[Release]):
        '''
        Исключение, поднимающееся, если не удалось найти релиз с тегом.

        :param tag: Тег релиза.
        :type tag: Tag
        :param releases: Список релизов.
        :type releases: list[Release]
        '''
        self.tag = tag
        self.releases = releases


    def __str__(self): return f'Не удалось найти релиз с тегом {self.tag.name}'


class GetNewReleasesError(Exception):
    def __init__(self, tag: Tag):
        '''
        Исключение, поднимающееся при ошибке получения информации о релизе.

        :param tag: Тег релиза.
        :type tag: Tag
        '''
        self.tag = tag


    def __str__(self): return f'Не удалось получить информацию о релизе с тегом {self.tag.name}'


class BackupNotFoundError(Exception):
    def __init__(self):
        '''
        Исключение, поднимающееся, если не найден распакованный бекап.
        '''


    def __str__(self): return 'Бекап не найден'


class InstallUpdateError(Exception):
    def __init__(self):
        '''
        Исключение, поднимающееся при ошибке во время установки обновления.
        '''


    def __str__(self): return 'Не удалось установить обновление Кардинала'


__all__ = [
    'ProxyCheckError',
    'GetBalanceError',
    'ProfileUpdateError',
    'ModuleImportError',
    'PluginNotTrustedException',
    'PluginDependenciesNotLoadedError',
    'CardinalNotInitializedError',
    'CardinalWorkerRunningError',
    'GitHubAPIUrlNotSpecified',
    'GitHubRequestError',
    'GetNextTagError',
    'ReleaseNotFoundError',
    'GetNewReleasesError',
    'BackupNotFoundError',
    'InstallUpdateError'
]