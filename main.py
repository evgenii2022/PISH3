import logging
from typing import Any

from agents.agents_dispatcher import AgentsDispatcher
from agents.scene import Scene
from entities.courier_entity import CourierEntity
from entities.order_entity import OrderEntity
from utils.excel_utils import get_excel_data, save_schedule_to_excel
from utils.json_utils import save_json

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    logging.info("Добро пожаловать в мир агентов")
    scene = Scene()
    dispatcher = AgentsDispatcher(scene)

    couriers = get_excel_data('Исходные данные.xlsx', 'Курьеры')
    logging.info(f'Прочитаны курьеры: {couriers}')
    for courier in couriers:
        onto_description: dict[str, Any] = {}
        entity = CourierEntity(onto_description, courier, scene)
        dispatcher.add_entity(entity)

    orders = get_excel_data('Исходные данные.xlsx', 'Заказы')
    logging.info(f'Прочитаны заказы: {orders}')
    for order in orders:
        onto_description: dict[str, Any] = {}
        entity = OrderEntity(onto_description, order, scene)
        dispatcher.add_entity(entity)

    all_schedule_records: list[dict[str, Any]] = []
    for courier in scene.get_entities_by_type('COURIER'):
        all_schedule_records.extend(courier.get_schedule_json())
    save_schedule_to_excel(all_schedule_records, 'Результаты.xlsx')
    save_json(all_schedule_records, '.', 'Результаты.json')
    
    #hello_agent = dispatcher.create_agent(Hello)
    
    while True:
        logging.info("A - добавить агента")
        logging.info("D - удалить агента")
        logging.info("L - посмотреть список агентов")
        logging.info("Q - Выход")
        user_input = input(": ")
        if user_input.upper() == "Q":
            break
        '''if user_input.upper() == "A":
            logging.info("Запускаем добавление агента")
            logging.info("Введите идентификатор агента")
            id_input = input(": ")
            hello_agent = dispatcher.create_agent(Hello, id_input)
            if not hello_agent:
                logging.info("Агент с таким идентификатором уже есть")
            else:
                logging.info("Aгент успешно создан")
        elif user_input.upper() == "D":
            logging.info("Запускаем удаление агента")
            logging.info("Введите идентификатор агента")
            id_input = input(": ")
            remove_result = dispatcher.remove_agent(id_input)
            logging.info(f'Результат удаления агента: {remove_result}')
        elif user_input.upper() == "L":
            agents_addresses = dispatcher.get_agents_id()
            logging.info(agents_addresses)
'''


