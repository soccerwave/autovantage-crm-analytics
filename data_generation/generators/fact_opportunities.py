import random
import numpy as np
import pandas as pd


def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]


def choose_lost_reason(stage: str) -> str | None:
    if stage != "Closed Lost":
        return None

    reasons = ["Competitor", "Price", "Delay", "No Decision"]
    weights = [0.38, 0.25, 0.19, 0.18]
    return random.choices(reasons, weights=weights, k=1)[0]


def build_converted_lead_opps(
    converted_leads_df: pd.DataFrame,
    dim_account: pd.DataFrame,
    dim_vehicle: pd.DataFrame,
    dim_date: pd.DataFrame,
    stage_probability_map: dict,
    stage_weights: dict,
    brand_discount_ranges: dict,
) -> list[dict]:
    account_ids = dim_account["account_id"].tolist()
    vehicle_brand_map = dict(zip(dim_vehicle["vehicle_id"], dim_vehicle["brand"]))
    vehicle_price_map = dict(zip(dim_vehicle["vehicle_id"], dim_vehicle["list_price_eur"]))
    valid_date_keys = dim_date["date_key"].tolist()

    records = []

    for idx, row in enumerate(converted_leads_df.itertuples(index=False), start=1):
        vehicle_id = row.vehicle_interest
        brand = vehicle_brand_map[vehicle_id]
        base_price = float(vehicle_price_map[vehicle_id])

        stage = weighted_choice(
            list(stage_weights.keys()),
            list(stage_weights.values()),
        )

        min_disc, max_disc = brand_discount_ranges[brand]
        if stage == "Closed Won":
            discount_pct = round(random.uniform(min_disc, max_disc), 2)
        elif stage == "Closed Lost":
            discount_pct = round(random.uniform(min_disc, max_disc + 2.0), 2)
        else:
            discount_pct = round(random.uniform(min_disc, max_disc - 1.0), 2)

        net_revenue = round(base_price * (1 - discount_pct / 100), 2)

        if brand == "BMW":
            sales_cycle_days = random.randint(18, 58)
        else:
            sales_cycle_days = random.randint(7, 38)

        created_date_key = int(row.created_date_key)

        close_date_key = None
        if stage in ["Closed Won", "Closed Lost"]:
            created_dt = pd.to_datetime(str(created_date_key), format="%Y%m%d")
            close_dt = created_dt + pd.Timedelta(days=sales_cycle_days)

            max_date = pd.to_datetime(str(max(valid_date_keys)), format="%Y%m%d")
            if close_dt > max_date:
                close_dt = max_date

            close_date_key = int(close_dt.strftime("%Y%m%d"))

        records.append({
            "opportunity_id": f"OPP-{idx:05d}",
            "lead_id": row.lead_id,
            "account_id": random.choice(account_ids),
            "contact_id": row.contact_id,
            "vehicle_id": vehicle_id,
            "dealer_id": row.dealer_id,
            "stage": stage,
            "deal_value_eur": round(base_price, 2),
            "discount_pct": discount_pct,
            "net_revenue_eur": net_revenue,
            "close_date_key": close_date_key,
            "sales_cycle_days": sales_cycle_days,
            "lost_reason": choose_lost_reason(stage),
            "probability_pct": stage_probability_map[stage],
        })

    return records


def build_direct_opps(
    start_index: int,
    row_count: int,
    dim_account: pd.DataFrame,
    dim_contact: pd.DataFrame,
    dim_vehicle: pd.DataFrame,
    dim_dealer: pd.DataFrame,
    dim_date: pd.DataFrame,
    stage_probability_map: dict,
    stage_weights: dict,
    brand_discount_ranges: dict,
) -> list[dict]:
    account_ids = dim_account["account_id"].tolist()
    contact_ids = dim_contact["contact_id"].tolist()
    dealer_ids = dim_dealer["dealer_id"].tolist()
    vehicle_ids = dim_vehicle["vehicle_id"].tolist()
    vehicle_brand_map = dict(zip(dim_vehicle["vehicle_id"], dim_vehicle["brand"]))
    vehicle_price_map = dict(zip(dim_vehicle["vehicle_id"], dim_vehicle["list_price_eur"]))
    valid_date_keys = dim_date["date_key"].tolist()

    records = []

    for idx in range(row_count):
        opp_id_num = start_index + idx
        vehicle_id = random.choice(vehicle_ids)
        brand = vehicle_brand_map[vehicle_id]
        base_price = float(vehicle_price_map[vehicle_id])

        stage = weighted_choice(
            list(stage_weights.keys()),
            list(stage_weights.values()),
        )

        min_disc, max_disc = brand_discount_ranges[brand]
        if stage == "Closed Won":
            discount_pct = round(random.uniform(min_disc, max_disc), 2)
        elif stage == "Closed Lost":
            discount_pct = round(random.uniform(min_disc, max_disc + 2.0), 2)
        else:
            discount_pct = round(random.uniform(min_disc, max_disc - 1.0), 2)

        net_revenue = round(base_price * (1 - discount_pct / 100), 2)

        if brand == "BMW":
            sales_cycle_days = random.randint(15, 60)
        else:
            sales_cycle_days = random.randint(5, 35)

        created_date_key = int(random.choice(valid_date_keys))

        close_date_key = None
        if stage in ["Closed Won", "Closed Lost"]:
            created_dt = pd.to_datetime(str(created_date_key), format="%Y%m%d")
            close_dt = created_dt + pd.Timedelta(days=sales_cycle_days)

            max_date = pd.to_datetime(str(max(valid_date_keys)), format="%Y%m%d")
            if close_dt > max_date:
                close_dt = max_date

            close_date_key = int(close_dt.strftime("%Y%m%d"))

        records.append({
            "opportunity_id": f"OPP-{opp_id_num:05d}",
            "lead_id": None,
            "account_id": random.choice(account_ids),
            "contact_id": random.choice(contact_ids),
            "vehicle_id": vehicle_id,
            "dealer_id": random.choice(dealer_ids),
            "stage": stage,
            "deal_value_eur": round(base_price, 2),
            "discount_pct": discount_pct,
            "net_revenue_eur": net_revenue,
            "close_date_key": close_date_key,
            "sales_cycle_days": sales_cycle_days,
            "lost_reason": choose_lost_reason(stage),
            "probability_pct": stage_probability_map[stage],
        })

    return records


def generate_fact_opportunities(
    target_row_count: int,
    seed: int,
    fact_leads: pd.DataFrame,
    dim_account: pd.DataFrame,
    dim_contact: pd.DataFrame,
    dim_vehicle: pd.DataFrame,
    dim_dealer: pd.DataFrame,
    dim_date: pd.DataFrame,
    stage_probability_map: dict,
    stage_weight_groups: dict,
    brand_discount_ranges: dict,
) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)

    converted_leads = fact_leads[fact_leads["is_converted"] == True].copy()

    direct_opp_target = round(target_row_count * 0.15)
    lead_based_target = target_row_count - direct_opp_target

    if len(converted_leads) < lead_based_target:
        raise ValueError(
            f"Not enough converted leads ({len(converted_leads)}) for required lead-based opportunities ({lead_based_target})."
        )

    sampled_converted = converted_leads.sample(n=lead_based_target, random_state=seed).copy()

    lead_based_records = build_converted_lead_opps(
        converted_leads_df=sampled_converted,
        dim_account=dim_account,
        dim_vehicle=dim_vehicle,
        dim_date=dim_date,
        stage_probability_map=stage_probability_map,
        stage_weights=stage_weight_groups["from_converted_leads"],
        brand_discount_ranges=brand_discount_ranges,
    )

    direct_records = build_direct_opps(
        start_index=len(lead_based_records) + 1,
        row_count=direct_opp_target,
        dim_account=dim_account,
        dim_contact=dim_contact,
        dim_vehicle=dim_vehicle,
        dim_dealer=dim_dealer,
        dim_date=dim_date,
        stage_probability_map=stage_probability_map,
        stage_weights=stage_weight_groups["direct_opps"],
        brand_discount_ranges=brand_discount_ranges,
    )

    df = pd.DataFrame(lead_based_records + direct_records)

    return df