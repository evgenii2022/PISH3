""" Перечень сообщений, которыми обмениваются агенты"""
from enum import Enum


class MessageType(Enum):
    """
    Перечень сообщений протокола планирования
    """
    INIT_MESSAGE = 'Инициализация'
    PRICE_REQUEST = 'Запрос цены'
    PRICE_RESPONSE = 'Ответ цены'
    PLANNING_REQUEST = 'Запрос на размещение'
    PLANNING_RESPONSE = 'Ответ на размещение'
