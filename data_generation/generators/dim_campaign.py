import random
import pandas as pd


def generate_dim_campaign(seed: int) -> pd.DataFrame:
    random.seed(seed)

    campaign_plan = (
        [("Email", 15)] +
        [("Social", 8)] +
        [("Event", 4)] +
        [("Paid Search", 3)]
    )

    records = []
    campaign_idx = 1

    for campaign_type, count in campaign_plan:
        for _ in range(count):
            if campaign_type == "Email":
                budget = random.randint(5000, 18000)
            elif campaign_type == "Social":
                budget = random.randint(12000, 35000)
            elif campaign_type == "Paid Search":
                budget = random.randint(20000, 50000)
            else:  # Event
                budget = random.randint(45000, 80000)

            records.append({
                "campaign_id": f"CMP-{campaign_idx:03d}",
                "campaign_name": f"{campaign_type} Campaign {campaign_idx}",
                "campaign_type": campaign_type,
                "budget_eur": budget,
                "status": random.choice(["Planned", "Active", "Completed"]),
                "channel_group": "Digital" if campaign_type in ["Email", "Social", "Paid Search"] else "Offline",
            })
            campaign_idx += 1

    df = pd.DataFrame(records)
    df["campaign_key"] = range(1, len(df) + 1)

    columns = [
        "campaign_key",
        "campaign_id",
        "campaign_name",
        "campaign_type",
        "budget_eur",
        "status",
        "channel_group",
    ]

    return df[columns]