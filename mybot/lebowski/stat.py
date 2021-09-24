import logging
import pandas as pd


def get_total_mileage(df_mileage: pd.DataFrame) -> int:
    try:
        total_mileage = df_mileage['mileage'].iloc[0] - df_mileage['mileage'].iloc[-1]
        return total_mileage
    except Exception as e:
        logging.error(e)
        return 0


def convert_spendings_to_eur(df_spending: pd.DataFrame, rates: dict) -> pd.DataFrame:
    def convert_to_eur(amount, ccy, rates):
        rate = 1.0
        try:
            rate = rates[ccy]
        except Exception as e:
            logging.error(e)
        return amount * 1.0 / rate

    df_spending['amount_eur'] = pd.Series(
        convert_to_eur(row.amount, row.ccy, rates) for row in df_spending.itertuples()
    )
    return df_spending


def get_total_spending_eur(df_spending: pd.DataFrame) -> float:
    try:
        total_spending = df_spending['amount_eur'].sum()
        return total_spending
    except Exception as e:
        logging.error(e)
        return 0.0