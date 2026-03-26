'В данном модуле описаны все кастомные исключения, используемые в пакете FunPayAPI.'
from __future__ import annotations


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Category
    from requests import Response


class AccountNotInitiatedError(Exception):
    def __init__(self):
        '''
        Исключение, поднимающееся при попытке вызвать метод класса Account без предварительного получения данных аккаунта с помощью метода Account.get.
        '''


    def __str__(self): return 'Необходимо получить данные об аккаунте с помощью метода Account.get()'


class BoundAccountRunnerError(Exception):
    def __init__(self):
        '''
        Исключение, поднимающееся если при инициализации Runner'а к аккаунту уже привязан другой Runner.
        '''


    def __str__(self): return 'К аккаунту уже привязан Runner'


class RequestFailedError(Exception):
    def __init__(self, response: Response):
        '''
        Исключение, поднимающееся при статус-коде ответа != 200.

        :param response: объект ответа.
        '''
        self.response = response

        self.status_code = response.status_code

        self.url = response.request.url

        self.request_headers = response.request.headers

        if 'cookie' in self.request_headers: self.request_headers['cookie'] = 'HIDDEN'

        self.request_body = response.request.body

        self.log_response = False


    def short_str(self): return f'Ошибка запроса к {self.url}. (Статус-код: {self.status_code})'


    def __str__(self):
        msg = (
            f'Ошибка запроса к {self.url}.\n'
            f'Метод: {self.response.request.method}.\n'
            f'Статус-код ответа: {self.status_code}.\n'
            f'Заголовки запроса: {self.request_headers}.\n'
            f'Тело запроса: {self.request_body}.\n'
            f'Текст ответа: {self.response.text}'
        )

        if self.log_response: msg+=f'\n{self.response.content.decode()}'


        return msg


class UnauthorizedError(RequestFailedError):
    def __init__(self, response):
        '''
        Исключение, поднимающееся, если не удалось найти идентифицирующий аккаунт элемент и/или произошло другое событие, указывающее на отсутствие авторизации.
        '''
        super().__init__(response)


    def short_str(self): return 'Не авторизирован (возможно, введен неверный golden_key?).'


class WithdrawError(RequestFailedError):
    def __init__(self, response, error_message: str | None):
        '''
        Исключение, поднимающееся при ошибке вывода средств с аккаунта.
        '''
        super().__init__(response)


        self.error_message = error_message

        if not self.error_message: self.log_response = True


    def short_str(self):
        msg = 'Ошибка при выводе средств с аккаунта'

        if self.error_message: msg+=f': {self.error_message}'


        return msg


class RaiseError(RequestFailedError):
    def __init__(self, response, category: Category, error_message: str | None, wait_time: int | None):
        '''
        Исключение, поднимающееся при ошибке поднятия лотов.
        '''
        super().__init__(response)


        self.category = category

        self.error_message = error_message

        self.wait_time = wait_time


    def short_str(self):
        msg = f'Не удалось поднять лоты категории "{self.category.name}"'

        if self.error_message: msg+=f': {self.error_message}' if self.error_message else ''


        return msg


class ImageUploadError(RequestFailedError):
    def __init__(self, response: Response, error_message: str | None):
        '''
        Исключение, поднимающееся при ошибке выгрузки изображения.
        '''
        super().__init__(response)


        self.error_message = error_message

        if not self.error_message: self.log_response = True


    def short_str(self):
        msg = f'Произошла ошибка при выгрузке изображения'

        if self.error_message: msg+=f': {self.error_message}'


        return msg


class MessageNotDeliveredError(RequestFailedError):
    def __init__(self, response: Response, error_message: str | None, chat_id: int):
        '''
        Исключение, поднимающееся при ошибке отправки сообщения.
        '''
        super().__init__(response)


        self.chat_id = chat_id

        self.error_message = error_message

        if not self.error_message: self.log_response = True


    def short_str(self):
        msg = f'Не удалось отправить сообщение в чат {self.chat_id}'

        if self.error_message: msg+=f': {self.error_message}'


        return msg


class FeedbackEditingError(RequestFailedError):
    def __init__(self, response: Response, error_message: str | None, order_id: str):
        '''
        Исключение, поднимающееся при ошибке добавления/редактирования/удаления отзыва/ответа на отзыв.
        '''
        super().__init__(response)


        self.order_id = order_id

        self.error_message = error_message

        if not self.error_message: self.log_response = True


    def short_str(self):
        msg = f'Не удалось изменить состояние отзыва / ответа на отзыв на заказ {self.order_id}'

        if self.error_message: msg+=f': {self.error_message}'


        return msg


class LotParsingError(RequestFailedError):
    def __init__(self, response: Response, error_message: str | None, lot_id: int):
        '''
        Исключение, поднимающееся при ошибке получения полей лота.
        '''
        super().__init__(response)


        self.lot_id = lot_id

        self.error_message = error_message

        if not self.error_message: self.log_response = True


    def short_str(self):
        msg = f'Не удалось получить данные лота {self.lot_id}'

        if self.error_message: msg+=f': {self.error_message}'


        return msg


class LotSavingError(RequestFailedError):
    def __init__(self, response: Response, error_message: str | None, lot_id: int, errors: dict[str, str]):
        '''
        Исключение, поднимающееся при ошибке сохранения лота.
        '''
        super().__init__(response)


        self.lot_id = lot_id

        self.errors = errors

        self.error_message = error_message

        if not self.error_message: self.log_response = True


    def short_str(self):
        msg = f'Не удалось сохранить лот {self.lot_id}'

        if self.error_message: msg+=f': {self.error_message}'


        return msg


class RefundError(RequestFailedError):

    def __init__(self, response: Response, error_message: str | None, order_id: str):
        '''
        Исключение, поднимающееся при ошибке возврата средств за заказ.
        '''
        super().__init__(response)


        self.order_id = order_id

        self.error_message = error_message

        if not self.error_message: self.log_response = True


    def short_str(self):
        msg = f'Не удалось вернуть средства по заказу {self.order_id}'

        if self.error_message: msg+=f': {self.error_message}'


        return msg


__all__ = [
    'AccountNotInitiatedError',
    'BoundAccountRunnerError',
    'RequestFailedError',
    'UnauthorizedError',
    'WithdrawError',
    'RaiseError',
    'ImageUploadError',
    'MessageNotDeliveredError',
    'FeedbackEditingError',
    'LotParsingError',
    'LotSavingError',
    'RefundError'
]