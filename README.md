# Exchange Rate Data Pipeline

An automated ETL data pipeline that fetches daily exchange rates, stores them in PostgreSQL, and provides trend analysis — running fully automated via GitHub Actions.

## Features

- 🔄 Automated daily data extraction from Frankfurter API (ECB reference rates)
- 💾 Idempotent data loading with upsert logic (no duplicate records on re-run)
- 📊 Trend analysis: day-over-day % change, 7-day min/max/average statistics
- ⚙️ Fully automated via GitHub Actions cron scheduling (no manual intervention needed)

## Tech Stack

- Python
- PostgreSQL (hosted on Supabase)
- SQLAlchemy
- GitHub Actions (CI/CD automation)
- Frankfurter API (free, open-source exchange rate data)

## Architecture
```
Frankfurter API → Python (Extract & Transform) → PostgreSQL (Load)
↑
GitHub Actions (Daily Scheduler)
```

## Database Schema

```sql
CREATE TABLE exchange_rates (
    id SERIAL PRIMARY KEY,
    base_currency VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    rate NUMERIC(12, 6) NOT NULL,
    rate_date DATE NOT NULL,
    fetched_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (base_currency, target_currency, rate_date)
);
```

## Scripts

| File | Purpose |
|------|---------|
| `fetch_rates.py` | Extracts exchange rates from API and loads into database (upsert) |
| `analyze.py` | Queries stored data to show latest rates, trends, and 7-day statistics |

## Running Locally

```bash
git clone https://github.com/Navanon-N18/data-pipeline.git
cd data-pipeline
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

Create a `.env` file:

DATABASE_URL=your_postgresql_connection_string


Run manually:
```bash
python fetch_rates.py
python analyze.py
```

## Automation

This pipeline runs automatically every day at 08:00 (Thailand time) via GitHub Actions. See `.github/workflows/fetch_rates.yml` for the schedule configuration.

## What I Learned

- Building an ETL (Extract, Transform, Load) pipeline from scratch
- Designing idempotent database operations using PostgreSQL's `ON CONFLICT DO UPDATE`
- Automating recurring tasks with GitHub Actions and cron scheduling
- Managing secrets securely in a CI/CD environment using GitHub Secrets
- Writing analytical SQL queries (aggregations, date filtering, trend comparison)

## Author

Navanon Phimngam — [LinkedIn](https://www.linkedin.com/in/navanon-phimngam-52307b308/) | [GitHub](https://github.com/Navanon-N18)