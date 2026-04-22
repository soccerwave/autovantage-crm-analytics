import random
import numpy as np
import pandas as pd


def clamp(value, low, high):
    return max(low, min(high, value))


def csat_to_nps(csat_score: int) -> int:
    if csat_score == 5:
        return random.choices([9, 10], weights=[0.45, 0.55], k=1)[0]
    if csat_score == 4:
        return random.choices([7, 8, 9], weights=[0.40, 0.45, 0.15], k=1)[0]
    if csat_score == 3:
        return random.choices([5, 6, 7], weights=[0.35, 0.45, 0.20], k=1)[0]
    if csat_score == 2:
        return random.choices([2, 3, 4, 5], weights=[0.25, 0.30, 0.25, 0.20], k=1)[0]
    return random.choices([0, 1, 2, 3], weights=[0.20, 0.30, 0.30, 0.20], k=1)[0]


def choose_comment(csat_score: int, breached: bool, reopened: bool) -> str:
    if csat_score >= 5:
        return random.choice([
            "Very smooth service experience",
            "Quick resolution and good communication",
            "Excellent support from the service team",
        ])
    if csat_score == 4:
        return random.choice([
            "Good overall service",
            "Issue solved with minor delays",
            "Satisfied but communication could improve",
        ])
    if csat_score == 3:
        return random.choice([
            "Average experience",
            "Problem solved but took longer than expected",
            "Service was acceptable",
        ])
    if reopened or breached:
        return random.choice([
            "Issue was not resolved properly the first time",
            "Resolution took too long",
            "Needed multiple follow-ups to get help",
            "Service delay caused frustration",
        ])
    return random.choice([
        "Not satisfied with the experience",
        "Communication was poor",
        "Expected better service quality",
    ])


def generate_fact_customer_feedback(
    seed,
    fact_service_cases: pd.DataFrame,
    dim_vehicle: pd.DataFrame,
    response_rate_by_priority: dict,
    brand_csat_adjustment: dict,
    brand_breach_penalty: dict,
) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)

    vehicle_brand_map = dict(zip(dim_vehicle["vehicle_id"], dim_vehicle["brand"]))

    records = []
    feedback_idx = 1

    for row in fact_service_cases.itertuples(index=False):
        if pd.isna(row.close_date_key):
            continue

        response_prob = response_rate_by_priority[row.priority]

        if row.is_reopened:
            response_prob -= 0.03

        if random.random() > response_prob:
            continue

        brand = vehicle_brand_map.get(row.vehicle_id, "Toyota")

        score_base = 4.2
        if row.is_sla_breached:
            score_base -= brand_breach_penalty[brand]

        if row.is_reopened:
            score_base -= 0.35

        if row.case_type == "Complaint":
            score_base -= 0.25

        if row.priority == "Critical":
            score_base -= 0.10

        score_base += brand_csat_adjustment[brand]
        score_base += np.random.normal(0, 0.55)

        rounded_csat = int(round(clamp(score_base, 1, 5)))
        rounded_csat = clamp(rounded_csat, 1, 5)

        nps_score = csat_to_nps(rounded_csat)
        comment = choose_comment(rounded_csat, row.is_sla_breached, row.is_reopened)

        records.append({
            "feedback_id": f"FDB-{feedback_idx:05d}",
            "case_id": row.case_id,
            "contact_id": row.contact_id,
            "dealer_id": row.dealer_id,
            "vehicle_id": row.vehicle_id,
            "survey_date_key": int(row.close_date_key),
            "csat_score": int(rounded_csat),
            "nps_score": int(nps_score),
            "comment_text": comment,
        })
        feedback_idx += 1

    return pd.DataFrame(records)