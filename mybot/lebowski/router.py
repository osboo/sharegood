import re
import logging
from lebowski.actions import add_gas_action
from lebowski.enums import CCY, BASIC_GAS_PRICE

gas_pattern = re.compile(r'(бензин)\s+(\d{1,3}\.?\d{0,2})\s*(\w{2,3})?\s*(\d{1,3}\.?\d{0,2})?\s*л?', re.IGNORECASE)
patterns = [gas_pattern]

def route(text: str) -> tuple:
    for pattern in patterns:
        match = re.match(pattern, text)
        if match is not None:
            if match.group(0).lower().startswith('бензин'):
                action = add_gas_action
                amount = float(match.group(2))
                ccy = CCY.from_string(match.group(3))
                volume = float(match.group(4)) if match.group(4) is not None else amount / BASIC_GAS_PRICE
                return (action, [amount, ccy, volume])

    raise ValueError(f"Cannot parse command {text}")

# route("Бензин 60.2") 
# https://regexr.com/6436v
