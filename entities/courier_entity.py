"""
Описание курьера.
"""
from dataclasses import dataclass

from entities.base_entity import BaseEntity
from entities.order_entity import OrderEntity
from point import Point
from typing import Any, Optional
from agents.scene import Scene

@dataclass
class ScheduleItem:
    """
    Класс записи расписания
    """
    order: OrderEntity
    start_time: int
    end_time: int
    cost: float
    all_params: dict


class CourierEntity(BaseEntity):
    """
    Класс заказа
    """
    def __init__(self, onto_desc: dict[str, Any], init_dict_data: dict[str, Any], scene: Optional[Scene]=None):
        super().__init__(onto_desc, scene)
        self.number = init_dict_data.get('Табельный номер')
        self.name = init_dict_data.get('ФИО')
        x1 = init_dict_data.get('Координата начального положения x')
        y1 = init_dict_data.get('Координата начального положения y')
        self.init_point = Point(x1, y1)
        self.types: list[str] = init_dict_data.get('Типы доставляемых заказов', '').split(';')
        
        self.types = [a.strip() for a in self.types]
        self.cost = init_dict_data.get('Стоимость выхода на работу')
        self.rate = init_dict_data.get('Цена работы за единицу времени')

        self.velocity = init_dict_data.get('Скорость')
        self.max_volume = init_dict_data.get('Объем ранца')
        self.max_mass = init_dict_data.get('Грузоподъемность')

        self.uri = 'Courier' + str(self.number)

        self.schedule: list[ScheduleItem] = []

    def __repr__(self):
        return 'Курьер ' + str(self.name)

    def get_type(self):
        """

        :return: onto_description -> metadata -> type
        """
        return 'COURIER'

    def get_conflicts(self, start_time: int, end_time: int) -> list[ScheduleItem]:
        """
        Возвращает записи, пересекающиеся по времени с запрошенным интервалом
        :param start_time:
        :param end_time:
        :return:
        """
        result = []
        for item in self.schedule:
            if start_time <= item.start_time < end_time or start_time < item.end_time <= end_time or \
                    item.start_time <= start_time < item.end_time or item.start_time < end_time <= item.end_time:
                result.append(item)
        return result

    def add_order_to_schedule(self, order: OrderEntity,
                              start_time: int, end_time: int, cost: float, all_params: dict) -> bool:
        """
        Добавляет заказ с параметрами в расписание
        :param order:
        :param start_time:
        :param end_time:
        :param cost:
        :param all_params
        :return:
        """
        schedule_item = ScheduleItem(order, start_time, end_time, cost, all_params)
        if not self.schedule:
            # Записей пока не было, добавляем заказ
            self.schedule.append(schedule_item)
            return True
        for item in self.schedule:
            if item.start_time <= start_time < item.end_time\
                    or item.start_time < end_time <= item.end_time:
                return False

        self.schedule.append(schedule_item)
        return True

    def get_last_point(self) -> Point:
        """
        Возвращает последнюю точку из расписания курьера
        :return:
        """
        if not self.schedule:
            return self.init_point
        last_point = self.schedule[-1].order.point_to
        return last_point

    def get_last_time(self) -> int:
        """
        Возвращает время, когда курьер может приступить к выполнению заказа
        :return:
        """
        if not self.schedule:
            return 0
        return self.schedule[-1].end_time

    def get_schedule_json(self):
        """
        Сериализация расписания курьера
        :return:
        """
        result = []
        for rec in self.schedule:
            json_record = {
                'resource_id': self.number,
                'resource_name': self.name,
                'task_id': rec.order.number,
                'task_name': rec.order.name,
                'start_time': rec.start_time,
                'end_time': rec.end_time,
                'cost': rec.cost,
            }
            result.append(json_record)
        return result
