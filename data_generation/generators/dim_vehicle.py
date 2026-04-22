import pandas as pd


def generate_dim_vehicle(
    toyota_models: list[str],
    volkswagen_models: list[str],
    bmw_models: list[str],
) -> pd.DataFrame:
    records = []

    toyota_prices = [
        18000, 22000, 26000, 32000, 30000,
        36000, 39000, 52000, 35000, 17000,
        34000, 70000, 28000, 33000, 48000,
    ]

    volkswagen_prices = [
        19000, 27000, 35000, 29000, 25000,
        38000, 41000, 52000, 24000, 69000,
        43000, 47000, 51000, 37000, 31000,
        45000, 58000, 28000, 40000, 16000,
    ]

    bmw_prices = [
        39000, 45000, 52000, 58000, 68000,
        48000, 62000, 82000, 71000, 85000,
    ]

    for idx, model in enumerate(toyota_models, start=1):
        records.append({
            "vehicle_id": f"VHL-{idx:03d}",
            "brand": "Toyota",
            "model_name": model,
            "segment": "Mass Market",
            "list_price_eur": toyota_prices[idx - 1],
        })

    start_idx = len(records) + 1
    for offset, model in enumerate(volkswagen_models, start=0):
        records.append({
            "vehicle_id": f"VHL-{start_idx + offset:03d}",
            "brand": "Volkswagen",
            "model_name": model,
            "segment": "Mass Market",
            "list_price_eur": volkswagen_prices[offset],
        })

    start_idx = len(records) + 1
    for offset, model in enumerate(bmw_models, start=0):
        records.append({
            "vehicle_id": f"VHL-{start_idx + offset:03d}",
            "brand": "BMW",
            "model_name": model,
            "segment": "Premium",
            "list_price_eur": bmw_prices[offset],
        })

    df = pd.DataFrame(records)
    df["vehicle_key"] = range(1, len(df) + 1)

    columns = [
        "vehicle_key",
        "vehicle_id",
        "brand",
        "model_name",
        "segment",
        "list_price_eur",
    ]

    return df[columns]