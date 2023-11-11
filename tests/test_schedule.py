from entities.courier_entity import CourierEntity
from entities.order_entity import OrderEntity


def test_get_conflicts():
    stub_courier = CourierEntity({}, {}, None)
    stub_order = OrderEntity({}, {}, None)

    result = stub_courier.add_order_to_schedule(stub_order, 5, 8, 20)
    assert result
    # Проверяем, что если записи не пересекаются, то конфликтов нет
    assert not stub_courier.get_conflicts(2, 4)
    assert not stub_courier.get_conflicts(2, 5)
    assert not stub_courier.get_conflicts(8, 10)
    assert not stub_courier.get_conflicts(9, 10)

    # Проверяем пересекающиеся записи
    conflicts = stub_courier.get_conflicts(2, 6)
    assert conflicts == [stub_courier.schedule[0]]
    conflicts = stub_courier.get_conflicts(6, 10)
    assert conflicts == [stub_courier.schedule[0]]
    conflicts = stub_courier.get_conflicts(5, 6)
    assert conflicts == [stub_courier.schedule[0]]
    conflicts = stub_courier.get_conflicts(6, 8)
    assert conflicts == [stub_courier.schedule[0]]
    conflicts = stub_courier.get_conflicts(6, 7)
    assert conflicts == [stub_courier.schedule[0]]
    conflicts = stub_courier.get_conflicts(5, 8)
    assert conflicts == [stub_courier.schedule[0]]
    conflicts = stub_courier.get_conflicts(2, 12)
    assert conflicts == [stub_courier.schedule[0]]
