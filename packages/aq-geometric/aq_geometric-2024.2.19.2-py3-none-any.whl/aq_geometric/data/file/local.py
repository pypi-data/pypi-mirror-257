from datetime import datetime

import pandas as pd


def load_hourly_data_from_fp(
    fp: str = "data.csv",
    verbose: bool = False,
) -> pd.DataFrame:
    """Load the dataframe from the database."""
    df = pd.read_csv(fp)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["aqsid"] = df["aqsid"].astype(str)

    if verbose: print(f"[{datetime.now()}] dataframe shape: {df.shape}")

    return df


def load_stations_info_from_fp(
    fp: str = "stations_info.csv",
    verbose: bool = False,
) -> pd.DataFrame:
    """Load the dataframe from the database."""
    df = pd.read_csv(fp)
    df["aqsid"] = df["aqsid"].astype(str)

    if verbose: print(f"[{datetime.now()}] dataframe shape: {df.shape}")

    return df
