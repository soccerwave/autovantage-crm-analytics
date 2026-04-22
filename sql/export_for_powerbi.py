from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "autovantage.duckdb"
OUT_DIR = PROJECT_ROOT / "powerbi_exports"
OUT_DIR.mkdir(exist_ok=True)

tables = [
    "raw_dim_date",
    "raw_dim_dealer",
    "raw_dim_vehicle",
    "raw_dim_campaign",
    "raw_fact_orders",
    "fct_pipeline",
    "fct_sales_funnel",
    "fct_case_resolution",
    "stg_customer_feedback",
    "fct_campaign_attribution",
]

con = duckdb.connect(str(DB_PATH))

for table in tables:
    out_file = OUT_DIR / f"{table}.csv"
    con.execute(
        f"""
        COPY {table}
        TO '{out_file.as_posix()}'
        (HEADER, DELIMITER ',');
        """
    )
    print(f"Exported: {out_file}")

con.close()
print("Done.")