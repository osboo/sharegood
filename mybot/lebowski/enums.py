import re

class CCY:
    BYN = "BYN"
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"

    @classmethod
    def from_string(cls, s):
        if s is None:
            return cls.BYN

        ccys = [
            (r'r[u,r][r,b]?', cls.RUB),
            (r'b[y,r]?n?', cls.BYN),
            (r'usd?', cls.USD),
            (r'eur?', cls.EUR),
        ]
        for ccy in ccys:
            m = re.match(ccy[0], s, re.IGNORECASE)
            if m is not None:
                return ccy[1]
        raise ValueError(f"Invalid currency string {s}, try rub, byn, usd, or eur")

class Tables:
    SPENDINGS = "spendings"
    MILEAGE = "mileage"
    REMINDERS = "reminders"

BASIC_GAS_PRICE = 2.05