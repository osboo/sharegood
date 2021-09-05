import pytest
from lebowski.router import route
from lebowski.actions import add_car_goods_action, add_car_repair_action, add_gas_action, add_mileage_action
from lebowski.enums import CCY

@pytest.mark.parametrize(
    "ccy,expected",
    [
        ("rur", CCY.RUB),
        ("Rur", CCY.RUB),
        ("Rub", CCY.RUB),
        ("rub", CCY.RUB),
        ("RUR", CCY.RUB),
        ("ru", CCY.RUB),
        ("Ru", CCY.RUB),
        ("RU", CCY.RUB),
        ("RR", CCY.RUB),
        ("BYN", CCY.BYN),
        ("byn", CCY.BYN),
        ("by", CCY.BYN),
        ("By", CCY.BYN),
        ("BY", CCY.BYN),
        ("br", CCY.BYN),
        ("Br", CCY.BYN),
        ("USD", CCY.USD),
        ("US", CCY.USD),
        ("usd", CCY.USD),
        ("us", CCY.USD),
        ("EUR", CCY.EUR),
        ("EUr", CCY.EUR),
        ("eu", CCY.EUR),
        ("eur", CCY.EUR),
    ]
)
def test_parse_currency(ccy, expected):
    assert CCY.from_string(ccy) == expected

@pytest.mark.parametrize(
    "action_name,amount,ccy,volume,text",
    [
        (add_gas_action.__name__, 60.2, CCY.BYN, None, "Бензин 60.2"),
        (add_gas_action.__name__, 60.2, CCY.BYN, None, "бензин 60.2"),
        (add_gas_action.__name__, 60.2, CCY.RUB, None, "бензин 60.2 Rub"),
        (add_gas_action.__name__, 60.2, CCY.RUB, 30.0, "бензин 60.2 rub 30л"),
        (add_gas_action.__name__, 60.0, CCY.BYN, None, "бензин 60"),
        (add_gas_action.__name__, 60.2, CCY.RUB, 30.0, "бензин 60.2 rub 30"),
        (add_gas_action.__name__, 60.2, CCY.RUB, 30.0, "бензин 60,2 rub 30"),
        (add_gas_action.__name__, 60.2, CCY.RUB, 30.0, "бензин 60.2 rub 30 Л"),
        (add_gas_action.__name__, 60.2, CCY.RUB, 30.23, "бензин 60.2 rub 30.23л"),
        (add_gas_action.__name__, 60.2, CCY.RUB, 30.3, "бензин 60.2 rub 30.3л"),
        (add_gas_action.__name__, 60.2, CCY.RUB, 30.3, "бензин 60.2 rub 30.3"),
        (add_gas_action.__name__, 60.2, CCY.RUB, 30.3, "бензин  60.2    rub  30.3    Л"),
        (add_gas_action.__name__, 60, CCY.BYN, 3.0, "бензин  60 byn  3  л"),
        (add_gas_action.__name__, 60, CCY.BYN, 3.0, "бензин  60  3  л")
    ]
)
def test_routing_gas_spendings(action_name, amount, ccy, volume, text):
    (action, args) = route(text)
    assert action.__name__ == action_name
    assert args[0] == amount
    assert args[1] == ccy
    assert args[2] == volume


@pytest.mark.parametrize(
    "action_name,mileage,text",
    [
        (add_mileage_action.__name__, 124024.0, "пробег 124024"),
        (add_mileage_action.__name__, 124024.0, "пробег 124024км"),
        (add_mileage_action.__name__, 124024.0, "пробег 124024 км"),
        (add_mileage_action.__name__, 124024.0, "Пробег 124024"),
        (add_mileage_action.__name__, 124024.0, "пробег 124024 Км"),
        (add_mileage_action.__name__, 124024.0, "пробег 124024 КМ"),
    ]
)
def test_routing_mileage(action_name, mileage, text):
    (action, args) = route(text)
    assert action.__name__ == action_name
    assert args[0] == mileage


@pytest.mark.parametrize(
    "action_name,amount,ccy,description,text",
    [
        (add_car_goods_action.__name__, 33, CCY.BYN, '', "Автотовары 33"),
        (add_car_goods_action.__name__, 33.35, CCY.BYN, '', "Автотовары 33.35"),
        (add_car_goods_action.__name__, 33, CCY.BYN, "огнетушитель", "Автотовары 33 огнетушитель"),
        (add_car_goods_action.__name__, 33.5, CCY.BYN, "огнетушитель", "Автотовары 33.5 огнетушитель"),
        (add_car_goods_action.__name__, 33.6, CCY.BYN, "огнетушитель", "Автотовары 33,6 огнетушитель"),
        (add_car_goods_action.__name__, 33.6, CCY.BYN, "огнетушитель", "Автотовары 33,6 Byn огнетушитель"),
        (add_car_goods_action.__name__, 33.6, CCY.BYN, "огнетушитель", "Автотовары 33,6 BYN огнетушитель"),
        (add_car_goods_action.__name__, 33.6, CCY.BYN, "огнетушитель, лопата", "Автотовары 33,6 BYN огнетушитель, лопата"),
        (add_car_goods_action.__name__, 33.6, CCY.RUB, "огнетушитель, лопата", "Автотовары 33,6 rub огнетушитель, лопата"),
        (add_car_goods_action.__name__, 33.6, CCY.RUB, "огнетушитель, лопата", "Автотовары 33,6 Ru огнетушитель, лопата"),
        (add_car_goods_action.__name__, 33.6, CCY.RUB, "огнетушитель, лопата", "Автотовары 33,6 rur огнетушитель, лопата"),
        (add_car_goods_action.__name__, 33.6, CCY.BYN, "огнетушитель, лопата", "Автотовары 33.6 огнетушитель, лопата"),
    ]
)
def test_routing_car_goods_spendings(action_name, amount, ccy, description, text):
    (action, args) = route(text)
    assert action.__name__ == action_name
    assert args[0] == amount
    assert args[1] == ccy
    assert args[2] == description



@pytest.mark.parametrize(
    "action_name,amount,ccy,description,text",
    [
        (add_car_repair_action.__name__, 1000, CCY.BYN, '', "ремонт 1000"),
        (add_car_repair_action.__name__, 1000.1, CCY.BYN, '', "ремонт 1000.1"),
        (add_car_repair_action.__name__, 1000.1, CCY.BYN, 'большое ТО', "ремонт 1000.1 большое ТО"),
        (add_car_repair_action.__name__, 1000.1, CCY.BYN, 'большое ТО', "ремонт 1000.1 byn большое ТО"),
        (add_car_repair_action.__name__, 1000.1, CCY.RUB, 'большое ТО', "ремонт 1000.1 rub большое ТО"),
        (add_car_repair_action.__name__, 1000.1, CCY.BYN, 'большое то', "ремонт 1000,1 большое то"),
        (add_car_repair_action.__name__, 1000.1, CCY.RUB, 'большое то', "ремонт 1000,1 rub большое то")
    ]
)
def test_routing_car_repair_spendings(action_name, amount, ccy, description, text):
    (action, args) = route(text)
    assert action.__name__ == action_name
    assert args[0] == amount
    assert args[1] == ccy
    assert args[2] == description