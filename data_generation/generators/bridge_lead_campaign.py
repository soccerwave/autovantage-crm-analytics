import random
import pandas as pd


def generate_bridge_lead_campaign(
    fact_leads: pd.DataFrame,
    dim_campaign: pd.DataFrame,
    seed: int,
    association_rules: dict,
) -> pd.DataFrame:
    random.seed(seed)

    campaign_ids = dim_campaign["campaign_id"].tolist()
    records = []
    seen_pairs = set()

    for row in fact_leads.itertuples(index=False):
        lead_source = row.lead_source
        rule = association_rules.get(
            lead_source,
            {"attach_probability": 0.05, "max_campaigns": 1},
        )

        if random.random() > rule["attach_probability"]:
            continue

        num_campaigns = random.randint(1, rule["max_campaigns"])
        selected_campaigns = random.sample(campaign_ids, k=min(num_campaigns, len(campaign_ids)))

        for campaign_id in selected_campaigns:
            pair = (row.lead_id, campaign_id)
            if pair in seen_pairs:
                continue

            records.append({
                "lead_id": row.lead_id,
                "campaign_id": campaign_id,
            })
            seen_pairs.add(pair)

    return pd.DataFrame(records)