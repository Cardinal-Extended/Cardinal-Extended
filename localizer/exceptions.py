'Здесь описаны ошибки локализатора.'
from pathlib import Path


__all__ = [
    'LocaleNotFoundError',
    'LocaleLoadError',
    'FormatError'
]


class LocaleNotFoundError(Exception):
    def __init__(self, locale_path: Path, locale_name: str):
        '''
        Исключение, поднимающееся при отсутствии файла локализации.

        :param locale_path: Путь к файлу локализации.
        :type locale_path: Path
        :param locale_name: Язык.
        :type locale_name: str
        '''
        self.locale_path = locale_path
        self.locale_name = locale_name


    def __str__(self): return f'Отсутствует файл локализации "{self.locale_name}" ({self.locale_path})'


class LocaleLoadError(Exception):
    def __init__(self, locale_path: Path, error: Exception):
        '''
        Исключение, поднимающееся при ошибке загрузки языка.

        :param locale_path: Путь к файлу локализации.
        :type locale_path: Path
        :param error: Изначальная ошибка.
        :type error: Exception
        '''
        self.locale_path = locale_path
        self.error = error


    def __str__(self): return f'Не удалось загрузить файл локализации {self.locale_path}: {self.error}'


class FormatError(Exception):
    def __init__(self, text: str, error: Exception, args: tuple | list | None = None, kwargs: dict | None = None):
        '''
        Исключение, поднимающееся при ошибке форматировании текста.

        :param text: Текст.
        :type text: str
        :param error: Изначальная ошибка.
        :type error: Exception
        '''
        self.text = text
        self.error = error
        self.args = args
        self.kwargs = kwargs


    def __str__(self): return f'Не удалось отформатировать строку "{self.text}" (args={self.args}; kwargs={self.kwargs}): {self.error}'