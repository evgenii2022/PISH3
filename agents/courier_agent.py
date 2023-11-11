""" Реализация класса агента курьера"""
import logging
from typing import Any, Union
from entities.courier_entity import CourierEntity

from entities.order_entity import OrderEntity
from point import Point

from .agent_base import AgentBase
from .messages import MessageType
from thespian.actors import ActorAddress


class CourierAgent(AgentBase):
    """
    Класс агента курьера
    """
    def __init__(self):
        super().__init__()
        self.name = 'Агент курьера'
        self.subscribe(MessageType.PRICE_REQUEST, self.handle_price_request)
        self.subscribe(MessageType.PLANNING_REQUEST, self.handle_planning_request)
        self.entity: CourierEntity

    def handle_price_request(self, message: tuple[MessageType, OrderEntity], sender: ActorAddress):
        order = message[1]
        params = self.__get_params(order)
        price_message = (MessageType.PRICE_RESPONSE, params)
        self.send(sender, price_message)

    def __get_params(self, order: OrderEntity) -> list:
        """
        Формирует возможные варианты размещения заказа
        :param order:
        :return:
        """
        if self.entity.max_mass < order.weight:
            logging.info(f'{self} - Не могу взять заказ {order}. Причина - большой вес')
            return []
        if self.entity.max_volume < order.volume:
            logging.info(f'{self} - Не могу взять заказ {order}. Причина - большой объем')
            return []
        if order.order_type not in self.entity.types:
            logging.info(f'{self} - Не могу взять заказ {order}. Причина - не мой тип заказов')
            return []
        
        logging.info(f'!!!!!!{self} - СМОГ взять заказ {order}')

        p1 = order.point_from
        # Надо посчитать стоимость выполнения заказа, сроки доставки
        last_point: Point = self.entity.get_last_point()
        distance_to_order = last_point.get_distance_to_other(p1)

        p2 = order.point_to
        distance_with_order = p1.get_distance_to_other(p2)
        time_to_order = distance_to_order / self.entity.velocity
        time_with_order = distance_with_order / self.entity.velocity
        duration = time_to_order + time_with_order

        price = duration * self.entity.rate
        logging.info(f'{self} - заказ {order} надо пронести {distance_with_order},'
                     f' к нему идти {distance_to_order}'
                     f'это займет {duration} и будет стоить {price}')

        last_time = self.entity.get_last_time()

        asap_time_from = last_time + time_to_order
        asap_time_to = asap_time_from + time_with_order
        # Вариант, при котором мы выполняем заказ как только можем
        asap_variant = {'courier': self.entity, 'time_from': asap_time_from, 'time_to': asap_time_to,
                        'price': price, 'order': order}
        params = [asap_variant]

        if asap_time_from < order.time_from:
            # Генерируем вариант, при котором мы заберем заказ вовремя
            jit_time_from = order.time_from - time_to_order
            jit_time_to = jit_time_from + time_with_order
            jit_from_variant = {'courier': self.entity, 'time_from': jit_time_from, 'time_to': jit_time_to,
                                'price': price, 'order': order}
            params.append(jit_from_variant)
        logging.info(params)
        return params

    def handle_planning_request(self, message: tuple[MessageType, dict[str, Any]], sender: ActorAddress):
        """
        Обработка сообщения с запросом на планирования.
        :param message:
        :param sender:
        :return:
        """
        params = message[1]
        # Пытаемся добавить заказ в свое расписание
        adding_result = self.entity.add_order_to_schedule(params.get('order'),
                                                          params.get('time_from'),
                                                          params.get('time_to'),
                                                          params.get('price'),
                                                          params)

        conflicted_records = self.entity.get_conflicts(params.get('time_from'), params.get('time_to'))
        # Что будем делать с конфликтами?

        logging.info(f'{self} получил запрос на размещение {params}, '
                     f'результат - {adding_result}, конфликты - {conflicted_records}')

        result_msg = (MessageType.PLANNING_RESPONSE, adding_result)
        self.send(sender, result_msg)
