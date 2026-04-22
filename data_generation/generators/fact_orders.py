import pandas as pd


def generate_fact_orders(fact_opportunities: pd.DataFrame) -> pd.DataFrame:
    closed_won = fact_opportunities[fact_opportunities["stage"] == "Closed Won"].copy()

    closed_won = closed_won.reset_index(drop=True)
    closed_won["order_id"] = [f"ORD-{i:05d}" for i in range(1, len(closed_won) + 1)]
    closed_won["order_date_key"] = closed_won["close_date_key"]
    closed_won["order_status"] = "Completed"

    columns = [
        "order_id",
        "opportunity_id",
        "lead_id",
        "account_id",
        "contact_id",
        "vehicle_id",
        "dealer_id",
        "order_date_key",
        "deal_value_eur",
        "discount_pct",
        "net_revenue_eur",
        "order_status",
    ]

    return closed_won[columns]