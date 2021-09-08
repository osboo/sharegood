import re
from lebowski.actions import add_gas_action, add_mileage_action, add_car_goods_action, add_car_repair_action, add_mileage_reminder_action
from lebowski.enums import CCY


gas_pattern = re.compile(r'(бензин)\s+(\d{1,3}[\.\,]?\d{0,2})\s*([a-zA-Z]{2,3})?\s*(\d{1,3}\.?\d{0,2})?\s*л?', re.IGNORECASE)
mileage_pattern = re.compile(r'(пробег)\s*(\d*)\s*(км)?', re.IGNORECASE)
car_goods_pattern = re.compile(r'(автотовары)\s*(\d*[\.\,]?\d{0,2})\s*([a-zA-Z]{2,3})?\s*(.*)', re.IGNORECASE)
car_repair_pattern = re.compile(r'(ремонт)\s*(\d*[\.\,]?\d{0,2})\s*([a-zA-Z]{2,3})?\s*(.*)', re.IGNORECASE)
reminder_mileage_pattern = re.compile(r'(напоминание)\s*(\d{1,7})\s*(км)?\s*(.*)', re.IGNORECASE)
patterns = [gas_pattern, mileage_pattern, car_goods_pattern, car_repair_pattern, reminder_mileage_pattern]

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
                action = add_mileage_action
                mileage = float(match.group(2))
                return (action, [mileage])
            elif match.group(0).lower().startswith('автотовары'):
                action = add_car_goods_action
                amount = float(match.group(2).replace(',', '.'))
                ccy = CCY.from_string(match.group(3))
                description = match.group(4)
                return (action, [amount, ccy, description])
            elif match.group(0).lower().startswith('ремонт'):
                action = add_car_repair_action
                amount = float(match.group(2).replace(',', '.'))
                ccy = CCY.from_string(match.group(3))
                description = match.group(4)
                return (action, [amount, ccy, description])
            elif match.group(0).lower().startswith('напоминание'):
                action = add_mileage_reminder_action
                target_mileage = int(match.group(2))
                description = match.group(4)
                return (action, [target_mileage, description])


    raise ValueError(f"Cannot parse command {text}")

# route("Бензин 60.2") 
# https://regexr.com/6436v
