"""Модуль с определением базовой сущности"""
from functools import lru_cache
from typing import Any


class BaseEntity:
    """Базовая сущность"""

    def __init__(self, onto_desc: dict[str, Any], scene=None):
        self.onto_description = onto_desc
        self.name: str = onto_desc.get('data', {}).get('label', {}).get('value')
        # self.uri = self.onto_description.get('uri')
        self.uri = 'UNKNOWN_URI'
        self.scene = scene

    def __repr__(self):
        return 'Entity ' + str(self.name)

    def get_relations(self):
        """
        Возвращает связи сущности в виде словаря.
        :return:
        """
        result = {}
        properties = self.onto_description.get('metadata', {}).get('properties', {})
        for prop_name, value in properties.items():
            _type = value.get('type')
            if _type == 'relation':
                result[prop_name] = self.get_chain('data', prop_name, 'value', 'uri')
        return result

    def get_type(self):
        """

        :return: onto_description -> metadata -> type
        """
        return 'UNKNOWN_TYPE'
        # return self.onto_description.get('metadata').get('type')

    def get_uri(self):
        """

        :return: onto_description -> uri
        """
        return self.uri

    def to_json(self):
        """
        Возвращает представление сущности для отображения в json.
        :return: Набор данных для дальнейшей сериализации.
        """
        return {'name': str(self.name), 'uri': self.get_uri()}

    @lru_cache(maxsize=None)
    def get_chain(self, *args, default=None, check=False):
        """
        Цепочки вызовов .get() занимают много места и их неудобно переносить на следующую строку.
        Этот метод сделан, чтобы этого избежать
        :example: uri = self.entity.get_chain('data', 'related_zone', 'value', 'uri')
        :param args: имена элементов для последовательного извлечения из onto_description
        :param default: значение по умолчанию, если элемент отсутствует в словаре.
        :param check: проверять наличие запрашиваемых элементов в onto_description
        :raise KeyError, если check=True и запрашиваемых данных нет в onto_description
        :return:
        """
        chain = self.onto_description
        chain_length = len(args)
        for number, element in enumerate(args):
            _default = {} if chain_length - number > 1 else default

            if check and element not in chain:
                raise KeyError(f'"{element}" not exist in onto_description of {self}')

            if hasattr(chain, 'get'):
                chain = chain.get(element, _default)
            else:
                break

        return chain

    def get_simple_value(self, param_name):
        """
        Возвращает значение параметра простого типа (не ссылку!)
        :param param_name:
        :return:
        """
        return self.get_chain('data', param_name, 'value')
