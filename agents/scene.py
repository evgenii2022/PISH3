""" Реализация класса сцены"""
from __future__ import annotations

from collections import defaultdict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.base_entity import BaseEntity 
    from entities.courier_entity import CourierEntity 
    from entities.order_entity import OrderEntity 

class Scene:
    """
    Класс сцены
    """
    def __init__(self):
        self.entities: defaultdict[str, list[CourierEntity | OrderEntity]] = defaultdict(list)

    def get_entities_by_type(self, entity_type: str) -> list[CourierEntity | OrderEntity]:
        return self.entities.get(entity_type, [])

    def get_entity_by_uri(self, uri):
        """
        Возвращает сущность по URI.
        :param uri:
        :return:
        """
        for entity_list in self.entities.values():
            for entity in entity_list:
                # TODO: узнать, что за entity
                if entity.get_uri() == uri:
                    return entity
        return None
