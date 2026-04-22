import pandas as pd


def generate_dim_dealer(dealers: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(dealers).copy()

    df["dealer_key"] = range(1, len(df) + 1)

    columns = [
        "dealer_key",
        "dealer_id",
        "dealer_name",
        "region",
        "brand",
    ]

    return df[columns]