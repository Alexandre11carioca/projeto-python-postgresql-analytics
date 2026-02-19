from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL", "postgresql+psycopg://analytics:analytics@localhost:5432/analytics_db")

BASE = Path(__file__).resolve().parent.parent
CSV = BASE / "data" / "incidentes.csv"
SCHEMA_SQL = BASE / "sql" / "01_schema.sql"

def main():
    engine = create_engine(DB_URL)

    with engine.begin() as conn:
        conn.execute(text(SCHEMA_SQL.read_text(encoding="utf-8")))

    df = pd.read_csv(CSV, parse_dates=["data_abertura", "data_fechamento"])

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE incidentes;"))

    df.to_sql("incidentes", engine, if_exists="append", index=False, method="multi", chunksize=5000)

    print("OK: CSV carregado no PostgreSQL!")
    print("Linhas:", len(df))

if __name__ == "__main__":
    main()
