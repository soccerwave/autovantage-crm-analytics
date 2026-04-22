import random
import numpy as np
import pandas as pd


def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]


def generate_fact_leads(
    row_count: int,
    seed: int,
    dim_date: pd.DataFrame,
    dim_dealer: pd.DataFrame,
    dim_vehicle: pd.DataFrame,
    dim_contact: pd.DataFrame,
    lead_source_config: dict,
    month_volume_multipliers: dict,
) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)

    dates_df = dim_date.copy()
    dates_df["month_weight"] = dates_df["month"].map(month_volume_multipliers)
    date_keys = dates_df["date_key"].tolist()
    date_weights = dates_df["month_weight"].tolist()

    source_names = list(lead_source_config.keys())
    source_weights = [lead_source_config[s]["volume_weight"] for s in source_names]

    dealer_ids = dim_dealer["dealer_id"].tolist()
    contact_ids = dim_contact["contact_id"].tolist()
    vehicle_ids = dim_vehicle["vehicle_id"].tolist()

    dealer_region_map = dict(zip(dim_dealer["dealer_id"], dim_dealer["region"]))

    records = []

    for idx in range(1, row_count + 1):
        created_date_key = weighted_choice(date_keys, date_weights)
        lead_source = weighted_choice(source_names, source_weights)
        source_cfg = lead_source_config[lead_source]

        dealer_id = random.choice(dealer_ids)
        contact_id = random.choice(contact_ids)
        vehicle_interest = random.choice(vehicle_ids)
        region = dealer_region_map[dealer_id]
        assigned_to_rep = f"REP-{random.randint(1, 24):02d}"

        response_hours = np.random.normal(
            loc=source_cfg["response_hours_mean"],
            scale=source_cfg["response_hours_std"],
        )
        response_hours = max(0.1, round(float(response_hours), 2))

        is_converted = random.random() < source_cfg["conversion_rate"]

        if is_converted:
            lead_status = "Converted"
            converted_date_key = created_date_key
            lost_reason = None
            age_at_close_days = random.randint(1, 45)
        else:
            lead_status = weighted_choice(
                ["New", "Working", "Qualified", "Lost"],
                [0.14, 0.28, 0.18, 0.40],
            )

            if lead_status == "Lost":
                lost_reason = weighted_choice(
                    list(source_cfg["lost_reason_weights"].keys()),
                    list(source_cfg["lost_reason_weights"].values()),
                )
                age_at_close_days = random.randint(1, 60)
            else:
                lost_reason = None
                age_at_close_days = random.randint(0, 30)

            converted_date_key = None

        records.append({
            "lead_id": f"LD-{idx:05d}",
            "created_date_key": int(created_date_key),
            "dealer_id": dealer_id,
            "contact_id": contact_id,
            "lead_source": lead_source,
            "lead_status": lead_status,
            "vehicle_interest": vehicle_interest,
            "assigned_to_rep": assigned_to_rep,
            "first_response_hours": response_hours,
            "is_converted": is_converted,
            "converted_date_key": converted_date_key,
            "opportunity_id": None,
            "lost_reason": lost_reason,
            "age_at_close_days": age_at_close_days,
            "region": region,
        })

    df = pd.DataFrame(records)

    return df