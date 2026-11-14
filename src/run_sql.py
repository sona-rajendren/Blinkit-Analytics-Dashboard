"""Load the raw CSVs into SQLite, run sql/queries.sql, and save each result.

Run from the project root:  python src/run_sql.py
Creates blinkit.db (git-ignored) and outputs/sql_results/query_01.csv ... query_09.csv
"""
import re
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW, OUT = ROOT / "data" / "raw", ROOT / "outputs" / "sql_results"
DB = ROOT / "blinkit.db"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    DB.unlink(missing_ok=True)
    with sqlite3.connect(DB) as con:
        for csv in sorted(RAW.glob("blinkit_*.csv")):
            pd.read_csv(csv).to_sql(csv.stem, con, index=False)
            print(f"loaded {csv.stem}")

        sql = (ROOT / "sql" / "queries.sql").read_text()
        # each query is introduced by a comment line like "-- 3. Revenue by product category"
        blocks = re.split(r"^-- (\d+)\. (.+)$", sql, flags=re.M)[1:]
        for num, title, body in zip(blocks[0::3], blocks[1::3], blocks[2::3]):
            result = pd.read_sql_query(body.strip().rstrip(";"), con)
            result.to_csv(OUT / f"query_{int(num):02d}.csv", index=False)
            print(f"\n-- {num}. {title}\n{result.head(5).to_string(index=False)}")


if __name__ == "__main__":
    main()
