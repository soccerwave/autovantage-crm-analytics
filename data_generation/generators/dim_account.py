import random
import pandas as pd


def generate_dim_account(
    contacts_df: pd.DataFrame,
    row_count: int,
    seed: int,
) -> pd.DataFrame:
    random.seed(seed)

    contact_ids = contacts_df["contact_id"].tolist()
    sampled_contact_ids = random.sample(contact_ids, row_count)

    records = []

    corporate_share = 0.22
    corporate_cutoff = int(row_count * corporate_share)

    for idx in range(1, row_count + 1):
        primary_contact_id = sampled_contact_ids[idx - 1]

        if idx <= corporate_cutoff:
            account_type = "Corporate"
            account_name = f"Company {idx:04d}"
            industry = random.choice([
                "Logistics",
                "Construction",
                "Retail",
                "Healthcare",
                "Hospitality",
                "Technology",
            ])
        else:
            account_type = "Individual"
            account_name = f"Individual Account {idx:04d}"
            industry = None

        records.append({
            "account_id": f"ACC-{idx:05d}",
            "account_name": account_name,
            "account_type": account_type,
            "primary_contact_id": primary_contact_id,
            "industry": industry,
            "country": "Spain",
            "is_active": random.choice([True, True, True, False]),
        })

    df = pd.DataFrame(records)
    df["account_key"] = range(1, len(df) + 1)

    columns = [
        "account_key",
        "account_id",
        "account_name",
        "account_type",
        "primary_contact_id",
        "industry",
        "country",
        "is_active",
    ]

    return df[columns]