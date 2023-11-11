""" Реализация класса агента заказа"""
import logging
from typing import Any, Union

from .agent_base import AgentBase
from .messages import MessageType
from thespian.actors import ActorAddress


class OrderAgent(AgentBase):
    """
    Класс агента заказа
    """
    def __init__(self):
        super().__init__()
        self.name = 'Агент заказа'
        self.subscribe(MessageType.PRICE_RESPONSE, self.handle_price_response)
        self.subscribe(MessageType.PLANNING_RESPONSE, self.handle_planning_response)

        self.unchecked_couriers: list[ActorAddress] = []
        self.possible_variants: list[dict[str, Any]] = []

        
    def handle_init_message(self, message, sender):
        super().handle_init_message(message, sender)
        # Ищем в системе ресурсы и отправляем им запросы
        self.__send_params_request()

    def __send_params_request(self):
        all_couriers = self.scene.get_entities_by_type('COURIER')
        # matching (отсечь курьеров, которые не смогут меня выполнить)
        logging.info(f'{self} - список ресурсов: {all_couriers}')
        for courier in all_couriers:
            courier_address = self.dispatcher.reference_book.get_address(courier)
            logging.info(f'{self} - адрес {courier}: {courier_address}')
            self.unchecked_couriers.append(courier_address)
            self.send(courier_address, (MessageType.PRICE_REQUEST, self.entity))

    def handle_price_response(self, message: tuple[MessageType, list[dict[str, Any]]], sender: ActorAddress):
        logging.info(f'{self} - получил сообщение {message}')
        courier_variants = message[1]
        
        if len(courier_variants) == 0:
            logging.info(f'{self} - Курьер {sender} не дал мне никаких вариантов. Вероятно потому, что ему не подходит мой заказ.')
            #return

        self.possible_variants.extend(courier_variants)
        self.unchecked_couriers.remove(sender)
        if not self.unchecked_couriers:
            self.__run_planning()

    def __evaluate_variants(self):
        """
        Оцениваем варианты по критериям и расширяем информацию о них
        :return:
        """
        if not self.possible_variants:
            return
        all_start_times = [var.get('time_from') for var in self.possible_variants]
        min_start_time = min(all_start_times)
        max_start_time = max(all_start_times)
        all_finish_times = [var.get('time_to') for var in self.possible_variants]
        min_finish_time = min(all_finish_times)
        max_finish_time = max(all_finish_times)
        all_prices = [var.get('price') for var in self.possible_variants]
        min_price = min(all_prices)
        max_price = max(all_prices)
        logging.info(f'{self} минимальный старт: {min_start_time}, минимальное завершение - {min_finish_time}, '
                     f'минимальная цена - {min_price}')
        for variant in self.possible_variants:
            start_efficiency = self.get_decreasing_kpi_value(variant.get('time_from'), min_start_time, max_start_time)
            finish_efficiency = self.get_increasing_kpi_value(variant.get('time_to'), min_finish_time, max_finish_time)
            price_efficiency = self.get_decreasing_kpi_value(variant.get('price'), min_price, max_price)
            variant['start_efficiency'] = start_efficiency
            variant['finish_efficiency'] = finish_efficiency
            variant['price_efficiency'] = price_efficiency

            variant['total_efficiency'] = 0.3 * price_efficiency + 0.4 * start_efficiency + 0.3 * finish_efficiency

    def __run_planning(self):
        if not self.possible_variants:
            logging.info(f'{self} - нет возможных вариантов для планирования')
            return
        # Оцениваем варианты
        self.__evaluate_variants()
        # Сортируем варианты
        self.possible_variants.sort(key=lambda x: x.get('price'))
        # Наилучший
        best_variant = self.possible_variants[0]
        # Адрес лучшего варианта
        best_variant_address = self.dispatcher.reference_book.get_address(best_variant.get('courier'))

        logging.info(f'{self} - лучшим вариантом признан {best_variant}, '
                     f'адрес - {best_variant_address}')
        request_message = (MessageType.PLANNING_REQUEST, best_variant)
        self.send(best_variant_address, request_message)

    def handle_planning_response(self, message: tuple[MessageType, bool], sender: ActorAddress):
        """
        Обработка сообщения с результатами планирования.
        :param message:
        :param sender:
        :return:
        """
        result = message[1]
        logging.info(f'{self} - получил {message}, результат - {result}')
        # Что делаем дальше?
        if result:
            logging.info(f'{self} доволен, ничего делать не надо')
            return
        # Ищем другой вариант для размещения
        # Возможно, правильнее было бы снова инициализировать варианты путем переговоров
        # Но мы попробуем другие варианты, которые у нас уже есть
        sorted_vars = sorted(self.possible_variants,
                             key=lambda x: x.get('price'))
        # Прошлый лучший вариант, который мы проверяли
        checked_variant = sorted_vars[0]
        self.possible_variants.pop(0)
        if not self.possible_variants:
            self.__send_params_request()
            return
        self.__run_planning()