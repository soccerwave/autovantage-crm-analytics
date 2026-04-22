from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data_generation" / "data" / "raw"
DB_PATH = PROJECT_ROOT / "autovantage.duckdb"

FILES = {
    "raw_dim_date": "dim_date.csv",
    "raw_dim_dealer": "dim_dealer.csv",
    "raw_dim_vehicle": "dim_vehicle.csv",
    "raw_dim_contact": "dim_contact.csv",
    "raw_dim_campaign": "dim_campaign.csv",
    "raw_dim_account": "dim_account.csv",
    "raw_fact_leads": "fact_leads.csv",
    "raw_fact_opportunities": "fact_opportunities.csv",
    "raw_fact_orders": "fact_orders.csv",
    "raw_fact_service_cases": "fact_service_cases.csv",
    "raw_fact_customer_feedback": "fact_customer_feedback.csv",
    "raw_bridge_lead_campaign": "bridge_lead_campaign.csv",
}

con = duckdb.connect(str(DB_PATH))

for table_name, file_name in FILES.items():
    csv_path = RAW_DIR / file_name
    con.execute(f"DROP TABLE IF EXISTS {table_name}")
    con.execute(
        f"""
        CREATE TABLE {table_name} AS
        SELECT * FROM read_csv_auto('{csv_path.as_posix()}', HEADER=TRUE)
        """
    )
    count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"{table_name}: {count}")

con.close()
print(f"Loaded raw tables into {DB_PATH}")