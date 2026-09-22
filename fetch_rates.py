import os
import requests
from datetime import date
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

BASE_CURRENCY = "USD"
TARGET_CURRENCIES = ["THB", "EUR", "GBP", "JPY"]


def fetch_exchange_rates():
    """ดึงอัตราแลกเปลี่ยนล่าสุดจาก Frankfurter API"""
    symbols = ",".join(TARGET_CURRENCIES)
    url = (
        f"https://api.frankfurter.dev/v1/latest?base={BASE_CURRENCY}&symbols={symbols}"
    )

    response = requests.get(url)
    response.raise_for_status()  # ถ้า API error จะ raise exception ทันที
    data = response.json()

    return data


def save_to_database(data):
    """บันทึกอัตราแลกเปลี่ยนลง database"""
    rate_date = data["date"]

    with engine.connect() as connection:
        for target_currency, rate in data["rates"].items():
            connection.execute(
                text("""
                    INSERT INTO exchange_rates (base_currency, target_currency, rate, rate_date)
                    VALUES (:base, :target, :rate, :rate_date)
                    ON CONFLICT (base_currency, target_currency, rate_date) 
                    DO UPDATE SET rate = :rate, fetched_at = NOW()
                """),
                {
                    "base": BASE_CURRENCY,
                    "target": target_currency,
                    "rate": rate,
                    "rate_date": rate_date,
                },
            )
        connection.commit()

    print(f"✅ Saved {len(data['rates'])} exchange rates for {rate_date}")


if __name__ == "__main__":
    data = fetch_exchange_rates()
    save_to_database(data)
