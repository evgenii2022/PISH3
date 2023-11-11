""" Класс сделан для примера работы с базой знаний,
необходимо будет добавить методы по аналогии с get_devices
"""

import json
import logging
import typing

import requests


class OntoManager:
    """
    Класс, реализующий работу с базой знаний.
    """

    def __init__(self, kb_url: str):
        self.session = requests.Session()
        self.session.headers['Content-type'] = 'application/json'
        self.ontology_address = kb_url
        self.__login()

    def __login(self):
        login_url = '/api/login'
        full_address = self.ontology_address + login_url
        data = {"UserName": "editor", "Password": "editor"}
        try:
            resp = self.session.post(full_address, json=data)  # pylint: disable=unused-variable
            # logging.debug(resp.content)
        except Exception as ex:  # pylint: disable=broad-except
            logging.error(f'Exception was handled: {ex}, url: {full_address}')

    def __get_api_data(self, api_address='/api/data/equery', params=None) -> dict:
        """
        Совершает GET-запрос с переданным адресом и параметрами и возвращает результат в виде json.
        :param api_address: адрес API
        :param params: параметры запроса
        :return: ответ от API в формате json
        """

        full_address = self.ontology_address + api_address
        try:
            logging.debug(f'Отправляем запрос на {full_address}, параметры: {params}')
            data = self.session.get(full_address, params=params, timeout=600).json()
            logging.debug('Данные получены')
        except requests.exceptions.ConnectionError as ex:
            logging.error(f'Exception was handled: {ex}, url: {full_address}')
            data = {}
        except json.decoder.JSONDecodeError as ex:
            logging.error(f'Exception was handled: {ex}, url: {full_address}')
            return {}

        except Exception as ex:  # pylint: disable=broad-except
            exc_type = type(ex)
            logging.error(f'Exception was handled: {ex} - {exc_type}, url: {full_address}')
            return {}
        return data

    def get_devices(self):
        """
        Возвращает список оборудования.
        :return:
        """
        params = {
            'query.ontologyUri': 'http://www.kg.ru/Production-Model',
            'query.typeUri': 'http://www.kg.ru/Production-ontology#Production-equipment'
        }
        return self.__get_api_data(params=params).get('items', [])

    def get_child_classes_uris(self, base_type, ontology_uri):
        """
        Возвращает список дочерних классов модели
        :param base_type:
        :param ontology_uri:
        :return:
        """
        api_address = '/api/entities/subjects/object'
        params = {
            'ontologyUri': ontology_uri,
            'objectUri': base_type
        }
        data = self.__get_api_data(api_address=api_address, params=params)
        return [record.get('uri') for record in data]

    def get_child_objects_uris(self, base_type, ontology_uri) -> list[str]:
        """
        Получает все сущности всех наследуемых типов по иерархии
        :param base_type:
        :param ontology_uri:
        :return:
        """
        api_address = '/api/entities/planner'
        params = {
            'ontologyUri': ontology_uri,
            'baseTypeUri': base_type
        }
        data = self.__get_api_data(api_address=api_address, params=params)
        return [record.get('uri') for record in data]
