import random
import numpy as np
import pandas as pd


def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]


def pick_resolution_hours(priority, sla_target, compliant):
    if compliant:
        if priority == "Critical":
            return round(random.uniform(0.5, 4.0), 2)
        if priority == "High":
            return round(random.uniform(2.0, 24.0), 2)
        if priority == "Medium":
            return round(random.uniform(6.0, 72.0), 2)
        return round(random.uniform(12.0, 168.0), 2)

    if priority == "Critical":
        return round(random.uniform(4.5, 10.0), 2)
    if priority == "High":
        return round(random.uniform(24.5, 48.0), 2)
    if priority == "Medium":
        return round(random.uniform(72.5, 120.0), 2)
    return round(random.uniform(168.5, 240.0), 2)


def choose_case_status(close_date_key):
    if pd.isna(close_date_key):
        return random.choices(
            ["Open", "In Progress"],
            weights=[0.38, 0.62],
            k=1,
        )[0]
    return random.choices(
        ["Resolved", "Closed"],
        weights=[0.35, 0.65],
        k=1,
    )[0]


def generate_fact_service_cases(
    row_count,
    seed,
    dim_date,
    dim_dealer,
    dim_vehicle,
    dim_contact,
    dim_account,
    service_case_type_weights,
    service_priority_weights,
    sla_target_hours,
    priority_compliance_base,
    region_compliance_adjustment,
    service_month_multipliers,
):
    random.seed(seed)
    np.random.seed(seed)

    dates_df = dim_date.copy()
    dates_df["month_weight"] = dates_df["month"].map(service_month_multipliers)
    date_keys = dates_df["date_key"].tolist()
    date_weights = dates_df["month_weight"].tolist()

    dealer_ids = dim_dealer["dealer_id"].tolist()
    dealer_region_map = dict(zip(dim_dealer["dealer_id"], dim_dealer["region"]))
    vehicle_ids = dim_vehicle["vehicle_id"].tolist()
    contact_ids = dim_contact["contact_id"].tolist()
    account_ids = dim_account["account_id"].tolist()

    case_types = list(service_case_type_weights.keys())
    case_type_weights = list(service_case_type_weights.values())

    priorities = list(service_priority_weights.keys())
    priority_weights = list(service_priority_weights.values())

    max_date = int(dim_date["date_key"].max())

    records = []

    for idx in range(1, row_count + 1):
        open_date_key = int(weighted_choice(date_keys, date_weights))
        dealer_id = random.choice(dealer_ids)
        region = dealer_region_map[dealer_id]
        vehicle_id = random.choice(vehicle_ids)
        contact_id = random.choice(contact_ids)
        account_id = random.choice(account_ids)

        case_type = weighted_choice(case_types, case_type_weights)
        priority = weighted_choice(priorities, priority_weights)
        sla_target = sla_target_hours[priority]

        compliance_prob = priority_compliance_base[priority] + region_compliance_adjustment[region]
        compliance_prob = min(max(compliance_prob, 0.05), 0.98)

        is_sla_breached = not (random.random() < compliance_prob)
        resolution_hours = pick_resolution_hours(priority, sla_target, not is_sla_breached)

        open_dt = pd.to_datetime(str(open_date_key), format="%Y%m%d")
        close_dt = open_dt + pd.Timedelta(hours=resolution_hours)

        if int(close_dt.strftime("%Y%m%d")) > max_date:
            close_date_key = None
        else:
            close_date_key = int(close_dt.strftime("%Y%m%d"))

        reopened = False
        reopen_count = 0

        if case_type in ["Warranty", "Complaint"]:
            reopen_draw = random.random()
            if reopen_draw < 0.02:
                reopened = True
                reopen_count = 2
            elif reopen_draw < 0.10:
                reopened = True
                reopen_count = 1

        related_case_id = None
        if reopened:
            related_case_id = f"CASE-REL-{idx:05d}"

        status = choose_case_status(close_date_key)

        records.append({
            "case_id": f"CASE-{idx:05d}",
            "contact_id": contact_id,
            "account_id": account_id,
            "vehicle_id": vehicle_id,
            "dealer_id": dealer_id,
            "open_date_key": open_date_key,
            "close_date_key": close_date_key,
            "case_type": case_type,
            "priority": priority,
            "sla_target_hours": sla_target,
            "resolution_hours": resolution_hours,
            "is_sla_breached": is_sla_breached,
            "is_reopened": reopened,
            "reopen_count": reopen_count,
            "related_case_id": related_case_id,
            "status": status,
        })

    return pd.DataFrame(records)