'Здесь описаны некоторые полезные функции Кардинала.'
import os


from . import exceptions


import requests


__all__ = [
    'check_proxy',
    'set_console_title'
]


def check_proxy(proxy: dict) -> requests.Response:
    '''
    Проверяет работоспособность прокси.

    :param proxy: Словарь с данными прокси.
    :type proxy: dict
    :raises exceptions.ProxyCheckError: Если возникла ошибка при проверке прокси.
    :return: Ответ запроса.
    :rtype: Response
    '''
    try: response = requests.get('https://api.ipify.org/', proxies=proxy, timeout=10)

    except: raise exceptions.ProxyCheckError(proxy)


    return response


def set_console_title(title: str) -> None:
    '''
    Изменяет название консоли для Windows.
    '''
    try:
        if os.name == 'nt':  # Windows
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(title)

    except: ...


    return