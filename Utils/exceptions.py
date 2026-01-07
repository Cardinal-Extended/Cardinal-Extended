'В данном модуле описаны все кастомные исключения кардинала.'
from __future__ import annotations


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Plugin
    from pathlib import Path


__all__ = [
    'ProxyCheckError',
    'ModuleImportError',
    'PluginNotTrustedException',
    'PluginDependenciesNotLoadedError'
]


class ProxyCheckError(Exception):
    def __init__(self, proxies: dict[str, str]):
        '''
        Исключение, поднимающееся при неудачной попытке проверки прокси.

        :param proxies: Прокси.
        :type proxies: dict[str, str]
        :param error: Изначальная ошибка.
        :type error: Exception
        '''
        self.proxies = proxies


    def __str__(self): return f'Ошибка при проверке прокси {self.proxies}'


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