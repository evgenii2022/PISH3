"""
Описание заказа.
"""
from typing import Any
from entities.base_entity import BaseEntity
from point import Point


class OrderEntity(BaseEntity):
    """
    Класс заказа
    """
    def __init__(self, onto_desc: dict[str, Any], init_dict_data, scene=None):
        super().__init__(onto_desc, scene)
        self.number: int = init_dict_data.get('Номер')
        self.name: str = init_dict_data.get('Наименование')
        self.weight: float = init_dict_data.get('Масса')
        self.volume: float = init_dict_data.get('Объем')
        self.price: float = init_dict_data.get('Стоимость')
        x1: float = init_dict_data.get('Координата получения x')
        y1: float = init_dict_data.get('Координата получения y')
        self.point_from = Point(x1, y1)
        x2: float = init_dict_data.get('Координата доставки x')
        y2: float = init_dict_data.get('Координата доставки y')
        self.point_to = Point(x2, y2)
        self.time_from: float = init_dict_data.get('Время получения заказа')
        self.time_to: float = init_dict_data.get('Время доставки заказа')
        self.order_type: str = init_dict_data.get('Тип заказа')

        self.uri = 'Order' + str(self.number)

        self.delivery_data = {
            'courier': None,
            'price': None,
            'time_from': None,
            'time_to': None,
        }

    def __repr__(self):
        return 'Заказ ' + str(self.name)

    def get_type(self):
        """

        :return: onto_description -> metadata -> type
        """
        return 'ORDER'
