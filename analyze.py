import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def show_latest_rates():
    """แสดงอัตราแลกเปลี่ยนล่าสุด"""
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT target_currency, rate, rate_date
            FROM exchange_rates
            WHERE rate_date = (SELECT MAX(rate_date) FROM exchange_rates)
            ORDER BY target_currency
        """))
        print("=== อัตราแลกเปลี่ยนล่าสุด (1 USD =) ===")
        for row in result:
            print(f"{row.target_currency}: {row.rate}  ({row.rate_date})")


def show_trend(currency="THB"):
    """เทียบอัตราแลกเปลี่ยนวันนี้กับเมื่อวาน (% เปลี่ยนแปลง)"""
    with engine.connect() as connection:
        result = connection.execute(
            text("""
            SELECT rate, rate_date
            FROM exchange_rates
            WHERE target_currency = :currency
            ORDER BY rate_date DESC
            LIMIT 2
        """),
            {"currency": currency},
        )

        rows = result.fetchall()

        if len(rows) < 2:
            print(f"\nยังมีข้อมูลไม่พอเปรียบเทียบ {currency} (ต้องมีอย่างน้อย 2 วัน)")
            return

        today_rate = rows[0].rate
        yesterday_rate = rows[1].rate
        change = today_rate - yesterday_rate
        percent_change = (change / yesterday_rate) * 100

        direction = (
            "📈 เพิ่มขึ้น" if change > 0 else "📉 ลดลง" if change < 0 else "คงที่"
        )

        print(f"\n=== แนวโน้ม USD/{currency} ===")
        print(f"เมื่อวาน ({rows[1].rate_date}): {yesterday_rate}")
        print(f"วันนี้ ({rows[0].rate_date}): {today_rate}")
        print(f"{direction} {abs(percent_change):.2f}%")


def show_weekly_stats(currency="THB"):
    """สถิติ 7 วันล่าสุด: ค่าสูงสุด ต่ำสุด เฉลี่ย"""
    with engine.connect() as connection:
        result = connection.execute(
            text("""
            SELECT MIN(rate) as min_rate, MAX(rate) as max_rate, AVG(rate) as avg_rate, COUNT(*) as days
            FROM exchange_rates
            WHERE target_currency = :currency
            AND rate_date >= CURRENT_DATE - INTERVAL '7 days'
        """),
            {"currency": currency},
        )

        row = result.fetchone()

        print(
            f"\n=== สถิติ USD/{currency} (7 วันล่าสุด, {row.days} วันที่มีข้อมูล) ==="
        )
        print(f"ต่ำสุด: {row.min_rate}")
        print(f"สูงสุด: {row.max_rate}")
        print(f"เฉลี่ย: {round(row.avg_rate, 4) if row.avg_rate else 'N/A'}")


if __name__ == "__main__":
    show_latest_rates()
    show_trend("THB")
    show_weekly_stats("THB")
