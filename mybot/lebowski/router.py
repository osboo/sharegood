import re
from lebowski.actions import add_gas_action, add_mileage_record_action
from lebowski.enums import CCY


gas_pattern = re.compile(r'(бензин)\s+(\d{1,3}[\.\,]?\d{0,2})\s*(\w{2,3})?\s*(\d{1,3}\.?\d{0,2})?\s*л?', re.IGNORECASE)
mileage_pattern = re.compile(r'(пробег)\s*(\d*)\s*(км)?', re.IGNORECASE)
patterns = [gas_pattern, mileage_pattern]

def route(text: str) -> tuple:
    for pattern in patterns:
        match = re.match(pattern, text)
        if match is not None:
            if match.group(0).lower().startswith('бензин'):
                action = add_gas_action
                amount = float(match.group(2).replace(',', '.'))
                ccy = CCY.from_string(match.group(3))
                volume = float(match.group(4)) if match.group(4) is not None else None
                return (action, [amount, ccy, volume])
            elif match.group(0).lower().startswith('пробег'):
                action = add_mileage_record_action
                mileage = float(match.group(2))
                return (action, [mileage])

    raise ValueError(f"Cannot parse command {text}")

# route("Бензин 60.2") 
# https://regexr.com/6436v