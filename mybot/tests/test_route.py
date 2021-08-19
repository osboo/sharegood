import pytest
from lebowski.router import route
from lebowski.actions import add_gas_action
from lebowski.enums import CCY, BASIC_GAS_PRICE

@pytest.mark.parametrize(
    "ccy,expected",
    [
        ("rur", CCY.RUR),
        ("Rur", CCY.RUR),
        ("Rub", CCY.RUR),
        ("rub", CCY.RUR),
        ("RUR", CCY.RUR),
        ("ru", CCY.RUR),
        ("Ru", CCY.RUR),
        ("RU", CCY.RUR),
        ("RR", CCY.RUR),
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
        (add_gas_action.__name__, 60.2, CCY.BYN, 60.2 / BASIC_GAS_PRICE, "Бензин 60.2"),
        (add_gas_action.__name__, 60.2, CCY.BYN, 60.2 / BASIC_GAS_PRICE, "бензин 60.2"),
        (add_gas_action.__name__, 60.2, CCY.RUR, 60.2 / BASIC_GAS_PRICE, "бензин 60.2 Rub"),
        (add_gas_action.__name__, 60.2, CCY.RUR, 30.0, "бензин 60.2 rub 30л"),
        (add_gas_action.__name__, 60.0, CCY.BYN, 60.0 / BASIC_GAS_PRICE, "бензин 60"),
        (add_gas_action.__name__, 60.2, CCY.RUR, 30.0, "бензин 60.2 rub 30"),
        (add_gas_action.__name__, 60.2, CCY.RUR, 30.0, "бензин 60.2 rub 30 Л"),
        (add_gas_action.__name__, 60.2, CCY.RUR, 30.23, "бензин 60.2 rub 30.23л"),
        (add_gas_action.__name__, 60.2, CCY.RUR, 30.3, "бензин 60.2 rub 30.3л"),
        (add_gas_action.__name__, 60.2, CCY.RUR, 30.3, "бензин 60.2 rub 30.3"),
        (add_gas_action.__name__, 60.2, CCY.RUR, 30.3, "бензин  60.2    rub  30.3    Л"),
        (add_gas_action.__name__, 60, CCY.BYN, 3.0, "бензин  60 byn  3  л")
    ]
)
def test_routing_gas_spendings(action_name, amount, ccy, volume, text):
    (action, args) = route(text)
    assert action.__name__ == action_name
    assert args[0] == amount
    assert args[1] == ccy
    assert abs(args[2]-volume) <= 1e-2