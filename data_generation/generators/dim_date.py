import pandas as pd


def generate_dim_date(start_date: str, end_date: str) -> pd.DataFrame:
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    df = pd.DataFrame({
        "date_key": dates.strftime("%Y%m%d").astype(int),
        "full_date": dates,
        "year": dates.year,
        "quarter": dates.quarter,
        "month": dates.month,
        "month_name": dates.strftime("%B"),
        "day": dates.day,
        "day_of_week": dates.dayofweek + 1,
        "day_name": dates.strftime("%A"),
        "week_of_year": dates.isocalendar().week.astype(int),
        "is_weekend": dates.dayofweek >= 5,
    })

    return df