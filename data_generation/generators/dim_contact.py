import random
import pandas as pd
from faker import Faker


def generate_dim_contact(row_count: int, seed: int) -> pd.DataFrame:
    fake = Faker()
    Faker.seed(seed)
    random.seed(seed)

    records = []

    for idx in range(1, row_count + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()

        records.append({
            "contact_id": f"CON-{idx:05d}",
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "email": fake.unique.email(),
            "phone": fake.phone_number(),
            "city": fake.city(),
            "postal_code": fake.postcode(),
            "country": "Spain",
            "is_active": random.choice([True, True, True, False]),
        })

    df = pd.DataFrame(records)
    df["contact_key"] = range(1, len(df) + 1)

    columns = [
        "contact_key",
        "contact_id",
        "first_name",
        "last_name",
        "full_name",
        "email",
        "phone",
        "city",
        "postal_code",
        "country",
        "is_active",
    ]

    return df[columns]