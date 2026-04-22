import duckdb

con = duckdb.connect("C:/Users/samir/Downloads/autovantage-crm-analytics/autovantage.duckdb")

for table in [
    "fct_sales_funnel",
    "fct_pipeline",
    "fct_case_resolution",
    "fct_campaign_attribution",
]:
    count = con.execute(f"select count(*) from {table}").fetchone()[0]
    print(table, count)

con.close()