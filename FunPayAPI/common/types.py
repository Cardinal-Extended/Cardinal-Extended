'В этом модуле описаны различные типы, датаклассы и перечисления FunPayAPI.'
from __future__ import annotations


from . import (
    DISCORD_RE, DEAR_VENDORS_RE, ORDER_PURCHASED_RE, ORDER_CONFIRMED_RE, NEW_FEEDBACK_RE, NEW_FEEDBACK_ANSWER_RE, FEEDBACK_CHANGED_RE, FEEDBACK_DELETED_RE, REFUND_RE,
    FEEDBACK_ANSWER_CHANGED_RE, FEEDBACK_ANSWER_DELETED_RE, ORDER_CONFIRMED_BY_ADMIN_RE, PARTIAL_REFUND_RE, ORDER_REOPENED_RE, REFUND_BY_ADMIN_RE, PRODUCTS_AMOUNT_RE,
    generate_random_tag
)


import re
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from time import time


__all__ = [
    'EventTypes',
    'MessageTypes',
    'OrderStatuses',
    'SubCategoryTypes',
    'Currencies',
    'Wallets',
    'Months',
    'BuyerViewing',
    'ChatShortcut',
    'Chat',
    'Message',
    'OrderShortcut',
    'Order',
    'Category',
    'SubCategory',
    'LotFields',
    'ChipOffer',
    'ChipFields',
    'LotPage',
    'SellerShortcut',
    'LotShortcut',
    'MyLotShortcut',
    'UserProfile',
    'Review',
    'Balance',
    'PaymentMethod',
    'CalcResult',
    'InitialChatEvent',
    'ChatsListChangedEvent',
    'LastChatMessageChangedEvent',
    'NewMessageEvent',
    'MessageEventsStack',
    'InitialOrderEvent',
    'OrdersListChangedEvent',
    'NewOrderEvent',
    'OrderStatusChangedEvent'
]

def __get_message_type_by_re(text: str) -> MessageTypes:
    '''
    Возвращает тип сообщения на основе регулярных выражений.

    :param text: Текст сообщения.
    :type text: str
    :return: Тип сообщения.
    :rtype: MessageTypes
    '''
    for message_type in MessageTypes:
        if message_type is MessageTypes.NON_SYSTEM: continue


        if message_type.value.search(text): return message_type


    return MessageTypes.NON_SYSTEM


# ---------------------------------------------------------------------------- #
#                             Перечисления (Enums)                             #
# ---------------------------------------------------------------------------- #
class EventTypes(Enum):
    '''
    В данном классе перечислены все типы событий FunPayAPI.
    '''
    INITIAL_CHAT = 1
    '''Обнаружен чат (при первом запросе Runner'а).'''

    CHATS_LIST_CHANGED = 2
    '''Список чатов и/или последнее сообщение одного/нескольких чатов изменилось.'''

    LAST_CHAT_MESSAGE_CHANGED = 3
    '''В чате изменилось последнее сообщение.'''

    NEW_MESSAGE = 4
    '''Обнаружено новое сообщение в истории чата.'''

    INITIAL_ORDER = 5
    '''Обнаружен заказ (при первом запросе Runner'а).'''

    ORDERS_LIST_CHANGED = 6
    '''Список заказов и/или статус одного/нескольких заказов изменился.'''

    NEW_ORDER = 7
    '''Новый заказ.'''

    ORDER_STATUS_CHANGED = 8
    '''Статус заказа изменился.'''


class MessageTypes(Enum):
    '''
    В данном классе перечислены все типы сообщений.
    '''
    NON_SYSTEM = 1
    '''Несистемное сообщение.'''


    ORDER_PURCHASED = ORDER_PURCHASED_RE
    '''Покупатель {buyer} оплатил заказ #{order_id}. Лот. X, не забудьте потом нажать кнопку «Подтвердить выполнение заказа» или
     «Подтвердить получение валюты».'''


    ORDER_CONFIRMED = ORDER_CONFIRMED_RE
    '''Покупатель X подтвердил успешное выполнение заказа #Y и отправил деньги продавцу Z.'''


    NEW_FEEDBACK = NEW_FEEDBACK_RE
    '''Покупатель X написал отзыв к заказу #Y.'''


    FEEDBACK_CHANGED = FEEDBACK_CHANGED_RE
    '''Покупатель X изменил отзыв к заказу #Y.'''


    FEEDBACK_DELETED = FEEDBACK_DELETED_RE
    '''Покупатель X удалил отзыв к заказу #Y.'''


    NEW_FEEDBACK_ANSWER = NEW_FEEDBACK_ANSWER_RE
    '''Продавец Z ответил на отзыв к заказу #Y.'''


    FEEDBACK_ANSWER_CHANGED = FEEDBACK_ANSWER_CHANGED_RE
    '''Продавец Z изменил ответ на отзыв к заказу #Y.'''


    FEEDBACK_ANSWER_DELETED = FEEDBACK_ANSWER_DELETED_RE
    '''Продавец Z удалил ответ на отзыв к заказу #Y.'''

    ORDER_REOPENED = ORDER_REOPENED_RE
    '''Заказ #Y открыт повторно.'''

    REFUND = REFUND_RE
    '''Продавец Z вернул деньги покупателю X по заказу #Y.'''

    PARTIAL_REFUND = PARTIAL_REFUND_RE
    '''Часть средств по заказу #Y возвращена покупателю.'''

    ORDER_CONFIRMED_BY_ADMIN = ORDER_CONFIRMED_BY_ADMIN_RE
    '''Администратор A подтвердил успешное выполнение заказа #Y и отправил деньги продавцу Z.'''

    DISCORD = DISCORD_RE
    '''Вы можете перейти в Discord. Внимание: общение за пределами сервера FunPay считается нарушением правил.'''

    DEAR_VENDORS = DEAR_VENDORS_RE
    '''Уважаемые продавцы, не доверяйте сообщениям в чате! Перед выполнением заказа всегда проверяйте наличие оплаты в разделе «Мои продажи».'''

    REFUND_BY_ADMIN = REFUND_BY_ADMIN_RE
    '''Администратор A вернул деньги покупателю X по заказу #Y.'''


class OrderStatuses(Enum):
    '''
    В данном классе перечислены все состояния заказов.
    '''
    PAID = 1
    '''Заказ оплачен и ожидает выполнения.'''
    CLOSED = 2
    '''Заказ закрыт.'''
    REFUNDED = 3
    '''Средства по заказу возвращены.'''


class SubCategoryTypes(Enum):
    '''
    В данном классе перечислены все типы подкатегорий.
    '''
    COMMON = 1
    '''Подкатегория со стандартными лотами.'''
    CURRENCY = 2
    '''Подкатегория с лотами игровой валюты (их нельзя поднимать).'''


class Wallets(Enum):
    '''
    В данном классе перечислены все кошельки для вывода средств с баланса FunPay.
    '''
    QIWI = 1
    '''Qiwi кошелек.'''
    BINANCE = 2
    '''Binance Pay.'''
    TRC = 3
    '''USDT TRC20.'''
    CARD_RUB = 4
    '''Рублевая банковская карта.'''
    CARD_USD = 5
    '''Долларовая банковская карта.'''
    CARD_EUR = 6
    '''Евро банковская карта.'''
    WEBMONEY = 7
    '''WebMoney WMZ.'''
    YOUMONEY = 8
    '''ЮMoney.'''



class Currencies(Enum):
    '''
    В данном классе перечислены все типы валют баланса FunPay.
    '''
    USD = '$'
    '''Доллар'''
    RUB = '₽'
    '''Рубль'''
    EUR = '€'
    '''Евро'''
    UNKNOWN = '¤'
    '''Неизвестная валюта'''


class Months(Enum):
    '''
    Названия месяцев на FunPay.
    '''
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12
    января = 1
    февраля = 2
    марта = 3
    апреля = 4
    мая = 5
    июня = 6
    июля = 7
    августа = 8
    сентября = 9
    октября = 10
    ноября = 11
    декабря = 12
    січня = 1
    лютого = 2
    березня = 3
    квітня = 4
    травня = 5
    червня = 6
    липня = 7
    серпня = 8
    вересня = 9
    жовтня = 10
    листопада = 11
    грудня = 12


# ---------------------------------------------------------------------------- #
#                                  Датаклассы                                  #
# ---------------------------------------------------------------------------- #

# ------------------------------ Объекты FunPay ------------------------------ #
@dataclass(unsafe_hash=True)
class BuyerViewing:
    '''
    Данный класс представляет поле 'Покупатель смотрит'
    '''
    buyer_id: int
    'Айди покупателя.'
    link: str | None = None
    'Ссылка на лот.'
    text: str | None = None
    'Текстовое описание лота.'
    tag: str | None = None
    'Тег события.'
    html: str | None = None
    'HTML-код блока просмотра.'


@dataclass(unsafe_hash=True)
class ChatShortcut:
    id: int
    'Айди чата.'
    name: str
    'Название чата (имя собеседника).'
    last_message_text: str
    'Текст последнего сообщения в чате (макс. 250 символов).'
    node_msg_id: int
    'Айди последнего сообщения в чате.'
    user_msg_id: int
    'Айди последнего прочитанного сообщения.'
    unread: bool
    'Флаг непрочитанного чата.'
    html: str
    'HTML-код виджета чата.'
    last_by_bot: bool | None = None
    'Отправлено ли последнее сообщение с помощью Account.send_message.'
    __last_message_type: MessageTypes | None = field(init=False, default=None)


    @property
    def last_message_type(self) -> MessageTypes:
        '''
        Тип последнего сообщения в чате на основе регулярных выражений
        '''
        if self.__last_message_type is None: self.__last_message_type = __get_message_type_by_re(self.last_message_text)


        return self.__last_message_type


@dataclass
class Chat:
    id: int
    'Айди чата.'
    name: str
    'Название чата (имя собеседника).'
    html: str
    'HTML-код чата.'
    messages: list[Message] = field(default_factory=list)
    'Последние 100 сообщений чата.'
    looking_link: str | None = None
    'Ссылка на лот, который смотрит собеседник.'
    looking_text: str | None = None
    'Название лота, который смотрит собеседник.'


    def __hash__(self): return hash((self.id, self.name, self.html, self.looking_link, self.looking_text))


@dataclass(unsafe_hash=True)
class Message:
    id: int
    'Айди сообщения.'
    text: str
    'Текст сообщения.'
    chat_id: int | str
    'Айди чата.'
    chat_name: str | None
    'Название чата.'
    interlocutor_id: int | None
    'Айди собеседника.'
    author: str | None
    'Автор сообщения.'
    author_id: int
    'Айди автора сообщения.'
    html: str
    'HTML-код сообщения.'
    buyer_viewing: BuyerViewing | None = None
    'Лот, который смотрит собеседник'
    by_bot: bool = False
    'Отправлено ли сообщение с помощью Account.send_message?'
    image_link: str | None = None
    'Ссылка на изображение в сообщении.'
    image_name: str | None = None
    'Название изображения.'
    badge: str | None = None
    'Текст бэйджика техподдержки или автовыдачи FunPay.'
    is_employee: bool = False
    'Является ли пользователь сотрудником?'
    is_support: bool = False
    'Наличие бэйджика поддержки.'
    is_moderation: bool = False
    'Наличие бэйджика модерации.'
    is_arbitration: bool = False
    'Наличие бэйджика арбитража.'
    is_autoreply: bool = False
    'Наличие бэйджика автоответа.'
    initiator_username: str | None = None
    'Ник пользователя, который выполнил действие (для системных сообщений).'
    initiator_id: int | None = None
    'Айди пользователя, который выполнил действие (для системных сообщений).'
    i_am_seller: bool | None = None
    'Являемся ли мы продавцом по заказу (для системных сообщений)?'
    i_am_buyer: bool | None = None
    'Являемся ли мы покупателем по заказу (для системных сообщений)?'
    __type: MessageTypes | None = field(init=False, default=None)


    @property
    def type(self) -> MessageTypes:
        '''
        Тип сообщения.
        '''
        if self.__type is None:
            if self.author_id == 0: self.__type = MessageTypes.NON_SYSTEM

            else: self.__type = __get_message_type_by_re(self.text)


        return self.__type


@dataclass(unsafe_hash=True)
class OrderShortcut:
    id: str
    'Айди заказа.'
    description: str
    'Описание заказа.'
    price: float
    'Цена заказа.'
    currency: Currencies
    'Валюта заказа.'
    buyer_username: str
    'Никнейм покупателя.'
    buyer_id: int
    'Айди покупателя.'
    chat_id: int | str
    'Айди чата.'
    status: OrderStatuses
    'Статус заказа.'
    date: datetime
    'Дата создания заказа.'
    subcategory_name: str
    'Название подкатегории, к которой относится заказ.'
    subcategory: SubCategory | None
    'Подкатегория, к которой относится заказ.'
    html: str
    'HTML-код виджета заказа.'
    __amount: int | None = field(init=False, default=None)


    @property
    def amount(self) -> int:
        '''
        Кол-во товаров (ищет по регулярному выражению).
        '''
        if self.__amount is None:
            result = [m.groupdict() for m in PRODUCTS_AMOUNT_RE.finditer(self.description)]

            self.__amount = int(result[0]['amount'].replace(" ", "")) if result else 1


        return self.__amount


@dataclass
class Order:
    id: str
    'Айди заказа.'
    status: OrderStatuses
    'Статус заказа.'
    subcategory: SubCategory | None
    'Подкатегория заказа.'
    lot_params: list[tuple[str, str]]
    'Параметры лота (значения некоторых полей заказа).'
    buyer_params: dict[str, str]
    'Параметры заказа, указанные покупателем.'
    title: str | None
    'Краткое описание (название) заказа. То же самое, что и title.'
    short_description: str | None
    'Краткое описание (название) заказа. То же самое, что и short_description.'
    full_description: str | None
    'Полное описание заказа.'
    amount: int
    'Количество.'
    sum: float
    'Сумма заказа.'
    currency: Currencies
    'Валюта заказа.'
    buyer_id: int
    'Айди покупателя.'
    buyer_username: str
    'Никнейм покупателя.'
    seller_id: int
    'Айди продавца.'
    seller_username: str
    'Никнейм продавца.'
    chat_id: str | int
    'Айди чата.'
    html: str
    'HTML-код заказа.'
    review: Review | None
    'Объект отзыва заказа.'
    order_secrets: list[str]
    'Список товаров автовыдачи FunPay заказа.'


    @property
    def lot_params_dict(self) -> dict[str, str]:
        '''
        Параметры лота из заказа в виде словаря.

        ВАЖНО!!! Если названия дублируются - часть данных будет утеряна.
        '''
        return {k: v for k, v in self.lot_params}


    def get_buyer_param(self, *args: str) -> str | None:
        '''
        Возвращает параметр, введенный покупателем по его названию.

        :return: Значение параметра.
        :rtype: str | None
        '''
        for param_name in args:
            if param_name in self.buyer_params: return self.buyer_params[param_name]


    def __hash__(self): return hash(
        (
            self.id,
            self.status,
            self.subcategory,
            self.title,
            self.short_description,
            self.full_description,
            self.amount,
            self.sum,
            self.currency,
            self.buyer_id,
            self.buyer_username,
            self.seller_id,
            self.seller_username,
            self.chat_id,
            self.html,
            self.review
        )
    )


@dataclass
class Category:
    id: int
    'Айди категории (game_id/data-id).'
    name: str
    'Название категории (игры).'
    subcategories: list[SubCategory] = field(default_factory=list)
    'Список подкатегорий.'
    position: int = 100_000
    'Порядковый номер игры в списке игр (по алфавиту).'


    @property
    def sorted_subcategories(self) -> dict[SubCategoryTypes, dict[int, SubCategory]]:
        '''
        Все подкатегории данной категории (игры) в виде словаря {type: {ID: подкатегория}}.
        '''
        sorted_subcategories: dict[SubCategoryTypes, dict[int, SubCategory]] = {
            SubCategoryTypes.COMMON: {},
            SubCategoryTypes.CURRENCY: {}
        }

        for subcategory in self.subcategories: sorted_subcategories[subcategory.type][subcategory.id] = subcategory


        return sorted_subcategories


    def add_subcategory(self, subcategory: SubCategory):
        '''
        Добавляет подкатегорию в список подкатегорий.

        :param subcategory: Объект подкатегории.
        :type subcategory: SubCategory
        '''
        if subcategory not in self.subcategories: self.subcategories.append(subcategory)


    def get_subcategory(self, subcategory_type: SubCategoryTypes, subcategory_id: int) -> SubCategory | None:
        '''
        Возвращает объект подкатегории.

        :param subcategory_type: Тип подкатегории.
        :type subcategory_type: SubCategoryTypes
        :param subcategory_id: Айди подкатегории.
        :type subcategory_id: int
        :return: Объект подкатегории.
        :rtype: SubCategory | None
        '''
        return self.sorted_subcategories[subcategory_type].get(subcategory_id)


    def __hash__(self): return hash((self.id, self.name, self.position))


@dataclass(unsafe_hash=True)
class SubCategory:
    id: int
    'Айди подкатегории.'
    name: str
    'Название подкатегории.'
    type: SubCategoryTypes
    'Тип подкатегории.'
    category: Category
    'Родительская категория (игра).'
    position: int = 100_000
    'Порядковый номер подкатегории в общем списке игр (для сортировки).'


    @property
    def fullname(self) -> str:
        'Полное название подкатегории.'
        return f'{self.name} {self.category.name}'


    @property
    def public_link(self) -> str:
        '''
        Публичная ссылка на список лотов подкатегории.
        '''
        return f'https://funpay.com/{'chips' if self.type is SubCategoryTypes.CURRENCY else 'lots'}/{self.id}/'


    @property
    def private_link(self) -> str:
        '''
        Приватная ссылка на список лотов подкатегории (для редактирования лотов).
        '''
        return f'{self.public_link}trade'


@dataclass
class __Fields:
    fields: dict[str, str]
    'Поля лота.'


    @property
    def csrf_token(self) -> str | None:
        'CSRF-токен.'
        return self.fields.get("csrf_token")

    @csrf_token.setter
    def csrf_token(self, csrf_token: str | None): self.fields['csrf_token'] = csrf_token if csrf_token is not None else ''


@dataclass
class LotFields(__Fields):
    lot_id: int
    'Айди лота.'
    subcategory: SubCategory | None = None
    'Подкатегория лота.'
    currency: Currencies = Currencies.UNKNOWN
    'Валюта лота.'
    calc_result: CalcResult | None = None
    'Ответ на запрос о рассчете комиссии раздела.'


    @property
    def title_ru(self) -> str:
        '''
        Русское краткое описание (название) лота.
        '''
        return self.fields.get('fields[summary][ru]', '')

    @title_ru.setter
    def title_ru(self, title_ru: str): self.fields['fields[summary][ru]'] = title_ru


    @property
    def title_en(self) -> str:
        '''
        Английское краткое описание (название) лота.
        '''
        return self.fields.get('fields[summary][en]', '')

    @title_en.setter
    def title_en(self, title_en: str): self.fields['fields[summary][en]'] = title_en


    @property
    def description_ru(self) -> str:
        '''
        Русское полное описание лота.
        '''
        return self.fields.get('fields[desc][ru]', '')

    @description_ru.setter
    def description_ru(self, description_ru: str): self.fields['fields[desc][ru]'] = description_ru


    @property
    def description_en(self) -> str:
        '''
        Английское полное описание лота.
        '''
        return self.fields.get('fields[desc][en]', '')

    @description_en.setter
    def description_en(self, description_en: str): self.fields['fields[desc][en]'] = description_en


    @property
    def payment_msg_ru(self) -> str:
        '''
        Русское сообщение покупателю после оплаты.
        '''
        return self.fields.get('fields[payment_msg][ru]', '')

    @payment_msg_ru.setter
    def payment_msg_ru(self, payment_msg_ru: str): self.fields['fields[payment_msg][ru]'] = payment_msg_ru


    @property
    def payment_msg_en(self) -> str:
        '''
        Английское сообщение покупателю после оплаты.
        '''
        return self.fields.get('fields[payment_msg][en]', '')

    @payment_msg_en.setter
    def payment_msg_en(self, payment_msg_en: str): self.fields['fields[payment_msg][en]'] = payment_msg_en


    @property
    def images(self) -> list[int]:
        '''
        Айди изображений лота.
        '''
        return [int(image) for image in self.fields.get("fields[images]", "").split(",") if image]

    @images.setter
    def images(self, images: list[int]): self.fields['fields[images]'] = ','.join([str(image) for image in images])


    @property
    def auto_delivery(self) -> bool:
        '''
        Включена ли автовыдача FunPay.
        '''
        return self.fields.get("auto_delivery") == "on"

    @auto_delivery.setter
    def auto_delivery(self, auto_delivery: bool): self.fields['auto_delivery'] = 'on' if auto_delivery else ''


    @property
    def secrets(self) -> list[str]:
        '''
        Товары автовыдачи FunPay.
        '''
        return [secret for secret in self.fields.get("secrets", "").strip().split("\n") if secret]

    @secrets.setter
    def secrets(self, secrets: list[str]): self.fields['secrets'] = "\n".join(secrets)


    @property
    def amount(self) -> int | None:
        '''
        Кол-во товара.
        '''
        return int(self.fields.get("amount")) if self.fields.get("amount") else None

    @amount.setter
    def amount(self, amount: int | None): self.fields['amount'] = str(amount) if amount is not None else ''


    @property
    def price(self) -> float | None:
        '''
        Цена за 1 шт.
        '''
        return float(price) if (price := self.fields.get("price")) else None

    @price.setter
    def price(self, price: float | None): self.fields['price'] = str(price) if price is not None else ''


    @property
    def active(self) -> bool:
        '''
        Активен ли лот.
        '''
        return self.fields.get("active") == "on"

    @active.setter
    def active(self, active: bool): self.fields['active'] = 'on' if active else ''


    @property
    def deactivate_after_sale(self) -> bool:
        '''
        Деактивировать ли лот после продажи.
        '''
        return self.fields.get("deactivate_after_sale") == "on"

    @deactivate_after_sale.setter
    def deactivate_after_sale(self, deactivate_after_sale: bool): self.fields['deactivate_after_sale'] = 'on' if deactivate_after_sale else ''


    @property
    def public_link(self) -> str:
        '''
        Публичная ссылка на лот.
        '''
        return f'https://funpay.com/lots/offer?id={self.lot_id}'


    @property
    def private_link(self) -> str:
        '''
        Приватная ссылка на лот (на изменение лота).
        '''
        return f'https://funpay.com/lots/offerEdit?offer={self.lot_id}'


    def __hash__(self): return hash((self.lot_id, self.subcategory, self.currency, self.calc_result))


@dataclass(unsafe_hash=True)
class ChipOffer:
    lot_id: str
    active: bool = False
    server: str | None = None
    side: str | None = None
    price: float | None = None
    amount: int | None = None


    @property
    def key(self):
        s = "".join([f"[{key}]" for key in self.lot_id.split("-")[3:]])
        return f"offers{s}"


@dataclass
class ChipFields(__Fields):
    account_id: int
    'Айди аккаунта FunPay.'
    subcategory_id: int
    'Айди подкатегории лота.'
    __chip_offers: dict[str, ChipOffer] = field(init=False, default_factory=dict)


    @property
    def min_sum(self) -> float | None:
        return float(self.fields.get('options[chip_min_sum]')) if self.fields.get('options[chip_min_sum]') else None

    @min_sum.setter
    def min_sum(self, min_sum: float | None): self.fields['options[chip_min_sum]'] = min_sum if min_sum else None


    @property
    def game_id(self) -> int:
        'Айди игры'
        return int(self.fields.get("game"))

    @game_id.setter
    def game_id(self, game_id: int): self.fields['game'] = str(game_id)


    @property
    def chip_offers(self) -> dict[str, ChipOffer]:
        if not self.__chip_offers:
            self.__chip_offers: dict[str, ChipOffer] = {}

            for k in self.fields:
                if not k.startswith('offers'): continue


                nums = re.findall(r'\d+', k)
                key = "-".join(list(map(str, nums)))

                offer_id = f"{self.account_id}-{self.game_id}-{self.subcategory_id}-{key}"

                if offer_id not in self.__chip_offers: self.__chip_offers[offer_id] = ChipOffer(offer_id)


                field = k.split("[")[-1].rstrip("]")

                v = self.fields[k]

                if field == "active": self.__chip_offers[offer_id].active = v == "on"
                elif field == "price": self.__chip_offers[offer_id].price = float(v) if v else None
                elif field == "amount": self.__chip_offers[offer_id].amount = int(v) if v else None


        return self.__chip_offers


    @chip_offers.setter
    def chip_offers(self, chip_offers: dict[str, ChipOffer]):
        self.__chip_offers = {}


        for chip_offer in chip_offers.values():
            key = chip_offer.key

            self.fields[f"{key}[amount]"] = str(chip_offer.amount) if chip_offer.amount is not None else ""

            self.fields[f"{key}[price]"] = str(chip_offer.price) if chip_offer.price is not None else ""

            if chip_offer.active: self.fields[f"{key}[active]"] = "on"

            else: self.fields.pop(f"{key}[active]", None)


    def __hash__(self): return hash((self.account_id, self.subcategory_id))


@dataclass
class LotPage:
    lot_id: int
    'Айди лота.'
    subcategory: SubCategory | None
    'Подкатегория.'
    short_description: str | None
    'Краткое описание.'
    full_description: str | None
    'Подробное описание.'
    image_urls: list[str]
    'Список URL-адресов изображений лота.'
    seller_id: int
    'Айди продавца.'
    seller_username: str
    'Юзернейм продавца.'


    @property
    def seller_url(self) -> str:
        """
        Cсылка на продавца.
        """
        return f"https://funpay.com/users/{self.seller_id}/"


    def __hash__(self): return hash((self.lot_id, self.subcategory, self.short_description, self.full_description, self.seller_id, self.seller_username))


@dataclass(unsafe_hash=True)
class SellerShortcut:
    id: int
    "ID пользователя."
    username: str
    "Никнейм пользователя."
    online: bool
    "Онлайн ли пользователь."
    stars: int | None
    "Количество звезд."
    reviews: int
    "Количество отзывов."
    html: str
    "HTML-код страницы пользователя."


    @property
    def link(self):
        '''
        Cсылка на продавца.
        '''
        return f"https://funpay.com/users/{self.id}/"


@dataclass
class LotShortcut:
    id: int | str
    'ID лота.'
    server: str | None
    "Название сервера (если указан)."
    side: str | None
    "Сторона (если указана)."
    title: str | None
    "Краткое описание (название) лота."
    description: str | None
    "Краткое описание (название) лота."
    amount: int | None
    "Количество"
    price: float
    "Цена лота."
    currency: Currencies
    "Валюта лота."
    subcategory: SubCategory | None
    "Подкатегория лота."
    seller: SellerShortcut | None
    "Объект продавца (только для лотов из талицы)."
    auto: bool
    "Включена ли автовыдача FunPay у лота?"
    promo: bool | None
    "В закрепе ли лот? (только для лотов из таблицы)"
    attributes: dict[str, int | str] | None
    "Атрибуты лота (только для лотов из таблицы)"
    html: str
    "HTML-код виджета лота."


    @property
    def public_link(self) -> str:
        '''
        Публичная ссылка на лот.
        '''
        return f"https://funpay.com/{'chips' if self.subcategory.type is SubCategoryTypes.CURRENCY else 'lots'}/offer?id={self.id}"


    def __hash__(self): return hash(
                (
                    self.id,
                    self.server,
                    self.side,
                    self.title,
                    self.description,
                    self.amount,
                    self.price,
                    self.currency,
                    self.subcategory,
                    self.seller,
                    self.auto,
                    self.promo,
                    self.html
                )
    )


@dataclass(unsafe_hash=True)
class MyLotShortcut:
    id: int | str
    "ID лота."
    server: str | None
    "Название сервера (если указан)."
    side: str | None
    "Сторона (если указана)."
    title: str | None
    "Краткое описание (название) лота."
    description: str | None
    "Краткое описание (название) лота."
    amount: int | None
    "Количество"
    price: float
    "Цена лота."
    currency: Currencies
    "Валюта лота."
    subcategory: SubCategory | None
    "Подкатегория лота."
    auto: bool
    "Включена ли автовыдача FunPay у лота?"
    active: bool
    "Активен ли лот?"
    html: str
    "HTML-код виджета лота."


    @property
    def public_link(self) -> str:
        '''
        Публичная ссылка на лот.
        '''
        return f"https://funpay.com/{'chips' if self.subcategory.type is SubCategoryTypes.CURRENCY else 'lots'}/offer?id={self.id}"


@dataclass(unsafe_hash=True)
class UserProfile:
    id: int
    "ID пользователя."
    username: str
    "Никнейм пользователя."
    profile_photo: str
    "Ссылка на фото профиля."
    online: bool
    "Онлайн ли пользователь."
    banned: bool
    "Заблокирован ли пользователь."
    html: str
    "HTML код страницы пользователя."
    __lots: dict[int | str, LotShortcut] = field(init=False, default_factory=dict)
    __sorted_by_subcategory_lots: dict[SubCategory, dict[int | str, LotShortcut]] = field(init=False, default_factory=dict)
    __sorted_by_subcategory_type_lots: dict[SubCategoryTypes, dict[int | str, LotShortcut]] = field(init=False, default_factory=dict)


    @property
    def lots(self) -> list[LotShortcut]:
        """
        Список всех лотов пользователя.
        """
        return list(self.__lots.values())


    @property
    def lots_dict(self) -> dict[int | str, LotShortcut]:
        '''
        Все лоты пользователя в виде словаря {ID: лот}}.
        '''
        return self.__lots


    @property
    def sorted_by_subcategory_lots(self) -> dict[SubCategory, dict[int | str, LotShortcut]]:
        '''
        Все лоты пользователя в виде словаря {подкатегория: {ID: лот}}.
        '''
        return self.__sorted_by_subcategory_lots


    @property
    def sorted_by_subcategory_type_lots(self) -> dict[SubCategoryTypes, dict[int | str, LotShortcut]]:
        '''
        Все лоты пользователя в виде словаря {Тип подкатегории: {ID: лот}}.
        '''
        if not self.__sorted_by_subcategory_type_lots: self.__sorted_by_subcategory_type_lots = {
            SubCategoryTypes.COMMON: {},
            SubCategoryTypes.CURRENCY: {}
        }


        return self.__sorted_by_subcategory_type_lots


    def get_lot(self, lot_id: int | str) -> LotShortcut | None:
        """
        Возвращает объект лота со страницы пользователя.

        :param lot_id: ID лота.
        :type lot_id: int | str

        :return: Объект лота со страницы пользователя.
        :rtype: LotShortcut | None
        """
        if isinstance(lot_id, str) and lot_id.isnumeric(): return self.__lots.get(int(lot_id))


        return self.__lots.get(lot_id)


    def update_lot(self, lot: LotShortcut) -> None:
        '''
        Обновляет лот в списке лотов.

        :param lot: Объект лота.
        :type lot: LotShortcut
        '''
        self.__lots[lot.id] = lot


        if lot.subcategory not in self.sorted_by_subcategory_lots: self.__sorted_by_subcategory_lots[lot.subcategory] = {}

        self.__sorted_by_subcategory_lots[lot.subcategory][lot.id] = lot


        if not self.__sorted_by_subcategory_type_lots: self.__sorted_by_subcategory_type_lots = {
            SubCategoryTypes.COMMON: {},
            SubCategoryTypes.CURRENCY: {}
        }

        self.__sorted_by_subcategory_type_lots[lot.subcategory.type][lot.id] = lot


    def add_lot(self, lot: LotShortcut) -> None:
        '''
        Добавляет лот в список лотов.

        :param lot: Объект лота.
        :type lot: LotShortcut
        '''
        if lot.id in self.lots_dict: return

        self.update_lot(lot)


    @property
    def common_lots(self) -> list[LotShortcut]:
        '''
        Возвращает список стандартных лотов со страницы пользователя.
        '''
        return list(self.sorted_by_subcategory_type_lots[SubCategoryTypes.COMMON].values())


    @property
    def currency_lots(self) -> list[LotShortcut]:
        '''
        Возвращает список лотов-валют со страницы пользователя.
        '''
        return list(self.sorted_by_subcategory_type_lots[SubCategoryTypes.CURRENCY].values())


@dataclass(unsafe_hash=True)
class Review:
    stars: int | None
    "Кол-во звезде в отзыве."
    text: str | None
    "Текст отзыва."
    reply: str | None
    "Текст ответа на отзыв."
    anonymous: bool
    "Анонимный ли отзыв?"
    html: str
    "HTML код отзыва."
    hidden: bool
    "Скрыт ли отзыв?"
    order_id: str | None = None
    "ID заказа, к которому относится отзыв."
    author: str | None = None
    "Автор отзыва."
    author_id: int | None = None
    "ID автора отзыва."
    by_bot: bool = False
    "Оставлен ли отзыв ботом?"
    reply_by_bot: bool = False
    "Оставлен ли ответ на отзыв ботом?"


@dataclass(unsafe_hash=True)
class Balance:
    total_rub: float
    "Общий рублёвый баланс."
    available_rub: float
    "Доступный к выводу рублёвый баланс."
    total_usd: float
    "Общий долларовый баланс."
    available_usd: float
    "Доступный к выводу долларовый баланс."
    total_eur: float
    "Общий евро баланс."
    available_eur: float
    "Доступный к выводу евро баланс."


@dataclass(unsafe_hash=True)
class PaymentMethod:
    name: str | None
    "Название."
    price: float
    "Цена (с комиссией)."
    currency: Currencies
    "Валюта."
    position: int | None
    "Позиция для сортировки."


@dataclass
class CalcResult:
    subcategory_type: SubCategoryTypes
    "Тип подкатегории."
    subcategory_id: int
    "ID подкатегории."
    methods: list[PaymentMethod]
    "Список платежных средств."
    price: float
    "Цена без комиссии."
    min_price_with_commission: float | None
    "Минимальная цена с комиссией из ответа FunPay, наличие не обязательно."
    min_price_currency: Currencies
    "Валюта минимальной цены."
    account_currency: Currencies
    "Валюта аккаунта."


    def get_coefficient(self, currency: Currencies) -> float:
        '''
        Отношение цены с комиссией в переданной валюте к цене без комиссии в валюте аккаунта.

        :param currency: Валюта.
        :type currency: Currencies
        :raises Exception: При ошибке определения коэффициента комиссии.
        :return: Коэффициент комиссии.
        :rtype: float
        '''
        if self.min_price_with_commission and (currency == self.min_price_currency == self.account_currency): return self.min_price_with_commission / self.price

        else:
            res = min(filter(lambda x: x.currency == currency, self.methods), key=lambda x: x.price, default=None)

            if not res: raise Exception("Невозможно определить коэффициент комиссии.") # TODO Custom Exception

            return res.price / self.price


    @property
    def commission_coefficient(self) -> float:
        """
        Отношение цены с комиссией к цене без комиссии в валюте аккаунта.
        """
        return self.get_coefficient(self.account_currency)


    @property
    def commission_percent(self) -> float:
        """
        Процент комиссии.
        """
        return (self.commission_coefficient - 1) * 100


    def __hash__(self): return hash((self.subcategory_type, self.subcategory_id, self.price, self.min_price_with_commission, self.min_price_currency, self.account_currency))


# ------------------------------ События FunPay ------------------------------ #
@dataclass
class BaseEvent:
    runner_tag: str
    '''Тег Runner'а.'''
    type: EventTypes
    'Тип события.'
    event_time: int | float = field(init=False, default_factory=time)
    'Время события.'


@dataclass(unsafe_hash=True)
class InitialChatEvent(BaseEvent):
    type: EventTypes = field(init=False, default=EventTypes.INITIAL_CHAT)
    'Тип события.'
    chat: ChatShortcut
    "Объект обнаруженного чата."


@dataclass(unsafe_hash=True)
class ChatsListChangedEvent(BaseEvent): # TODO: добавить список всех чатов.
    type: EventTypes = field(init=False, default=EventTypes.CHATS_LIST_CHANGED)
    'Тип события.'


@dataclass(unsafe_hash=True)
class LastChatMessageChangedEvent(BaseEvent):
    type: EventTypes = field(init=False, default=EventTypes.LAST_CHAT_MESSAGE_CHANGED)
    'Тип события.'
    chat: ChatShortcut
    "Объект чата, в котором изменилось последнее сообщение."


@dataclass
class NewMessageEvent(BaseEvent):
    type: EventTypes = field(init=False, default=EventTypes.NEW_MESSAGE)
    'Тип события.'
    message: Message
    "Объект нового сообщения."
    stack: MessageEventsStack
    "Объект стека событий новых сообщений."


@dataclass
class MessageEventsStack:
    id: str = field(init=False, default_factory=generate_random_tag)
    'Айди стека.'
    stack: list[NewMessageEvent] = field(init=False, default_factory=list)


    def add_events(self, messages: list[NewMessageEvent]) -> None:
        """
        Добавляет события новых сообщений в стэк.

        :param messages: список событий новых сообщений.
        :type messages: list[NewMessageEvent]
        """
        self.stack.extend(messages)


    def __hash__(self): return hash((self.id,))


@dataclass(unsafe_hash=True)
class InitialOrderEvent(BaseEvent):
    type: EventTypes = field(init=False, default=EventTypes.INITIAL_ORDER)
    'Тип события.'
    order: OrderShortcut
    "Объект обнаруженного заказа."


@dataclass(unsafe_hash=True)
class OrdersListChangedEvent(BaseEvent):
    type: EventTypes = field(init=False, default=EventTypes.ORDERS_LIST_CHANGED)
    'Тип события.'
    purchases: int
    "Кол-во незавершенных покупок."
    sales: int
    "Кол-во незавершенных продаж."


@dataclass(unsafe_hash=True)
class NewOrderEvent(BaseEvent):
    type: EventTypes = field(init=False, default=EventTypes.NEW_ORDER)
    'Тип события.'
    order: OrderShortcut
    "Объект нового заказа."


@dataclass(unsafe_hash=True)
class OrderStatusChangedEvent(BaseEvent):
    type: EventTypes = field(init=False, default=EventTypes.ORDER_STATUS_CHANGED)
    'Тип события.'
    order: OrderShortcut
    "Объект измененного заказа."