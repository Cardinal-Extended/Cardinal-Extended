'В этом модуле описаны различные датаклассы кардинала.'
from __future__ import annotations


from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Callable, Literal


__all__ = [
    'Plugin',
    'Handler'
]


@dataclass
class Plugin:
    'Класс, описывающий плагин кардинала.'
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
    'Класс, описывающий хендлер кардинала.'
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