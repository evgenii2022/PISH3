"""Содержит класс диспетчера агентов"""
import logging
import typing

from thespian.actors import ActorSystem, ActorExitRequest

from agents.courier_agent import CourierAgent
from agents.messages import MessageType
from agents.order_agent import OrderAgent
from agents.reference_book import ReferenceBook
from agents.scene import Scene
from entities.base_entity import BaseEntity

# В зависимости от типа сущности мы выбираем класс агента
TYPES_AGENTS = {
    'ORDER': OrderAgent,
    'COURIER': CourierAgent,
}


class AgentsDispatcher:
    def __init__(self, scene: Scene):
        self.actor_system = ActorSystem()
        self.reference_book = ReferenceBook()
        self.scene = scene

    def add_entity(self, entity: BaseEntity):
        """
        Добавляет сущность в сцену, создает агента и отправляет ему сообщение об инициализации
        :param entity:
        :return:
        """
        entity_type = entity.get_type()
        agent_type = TYPES_AGENTS.get(entity_type)
        if not agent_type:
            logging.warning(f'Для сущности типа {entity_type} не указан агент')
            return False
        self.scene.entities[entity_type].append(entity)
        self.create_agent(agent_type, entity)
        return True

    def create_agent(self, agent_class: type, entity: BaseEntity):
        agent = self.actor_system.createActor(agent_class)
        self.reference_book.add_agent(entity=entity, agent_address=agent)
        init_data = {'dispatcher': self, 'scene': self.scene, 'entity': entity}
        init_message = (MessageType.INIT_MESSAGE, init_data)
        self.actor_system.tell(agent, init_message)

    def remove_agent(self, entity_uri) -> bool:
        """
        Удаляет агента из сцены
        :param entity_uri:
        :return:
        """
        entity = self.scene.get_entity_by_uri(entity_uri)
        if not entity:
            logging.error(f'В сцене нет сущности с uri {entity_uri}')
            return False
        agent_address = self.reference_book.get_address(entity)
        if not agent_address:
            logging.error(f'Агент с идентификатором {entity} не найден')
            return False
        self.actor_system.tell(agent_address, ActorExitRequest())
        return True

    def get_agents_id(self) -> list:
        result = list(self.reference_book.agents_entities.keys())
        return result

    def get_agents_addresses(self) -> list:
        result = list(self.reference_book.agents_entities.values())
        return result
