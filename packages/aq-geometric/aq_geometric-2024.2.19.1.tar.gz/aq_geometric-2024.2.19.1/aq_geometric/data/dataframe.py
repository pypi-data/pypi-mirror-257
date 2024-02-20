from datetime import datetime
from typing import Union, Callable, List, Tuple

import h3
import numpy as np
import pandas as pd


def process_df(
    df: pd.DataFrame,
    stations_info: pd.DataFrame,
    start_time: str = "2020-01-01",
    end_time: str = "2024-01-01",
    time_step: str = "1H",
    aggregation_method: Union[Callable, str] = lambda x: np.mean(x[x >= 0])
    if len(x[x >= 0]) > 0 else -1,
    nan_value: Union[float, int] = -1,
    time_closed_interval: bool = False,
    verbose: bool = False,
) -> pd.DataFrame:
    """Take the raw DataFrame from the database and process it into a fixed-station, fixed-index format."""
    # make a datetime index for the full range
    date_range = pd.date_range(
        start=start_time, end=end_time, freq=time_step,
        inclusive="left" if time_closed_interval else "both")

    if verbose: print(f"[{datetime.now()}] processing dataframe")

    # we would like df to be indexed on time and have columns for each station
    df = df[["aqsid", "timestamp",
             "value"]].groupby(["timestamp", "aqsid"]).aggregate({
                 "value":
                 aggregation_method
             }).reset_index().pivot(index="timestamp", columns="aqsid",
                                    values="value").reindex(date_range)
    # undo the pivot so that we have a column for timestamp, a column for aqsid, and a column for value
    df = df.unstack().reset_index().rename(columns={
        "level_1": "timestamp",
        0: "value"
    })
    # join the lat, lon, elevation information to the main dataframe
    stations_info = stations_info.groupby("aqsid").first()
    df = df.join(stations_info, on="aqsid", how="inner")

    if verbose: print(f"[{datetime.now()}] dataframe shape: {df.shape}")

    # fill missing values with negative 1
    df = df.fillna(nan_value)

    return df


def process_feature(
    df: pd.DataFrame,
    start_time: str,
    end_time: str,
    aggregation_method: Union[Callable, str],
    min_h3_resolution: int,
    leaf_h3_resolution: int,
    include_root_node: bool = True,
    time_closed_interval: bool = False,
    verbose: bool = False,
) -> np.ndarray:
    """Process a single feature DataFrame to a set of node-level features."""
    # ensure that the columns exist
    assert "timestamp" in df.columns
    assert "latitude" in df.columns
    assert "longitude" in df.columns
    assert "aqsid" in df.columns
    assert "value" in df.columns

    # get the features from start time to end time
    if time_closed_interval:
        df = df[(df.timestamp >= start_time)
                & (df.timestamp <= end_time)].copy(deep=True)
    else:
        df = df[(df.timestamp >= start_time)
                & (df.timestamp < end_time)].copy(deep=True)
    df.reset_index(inplace=True)

    if verbose: print(f"[{datetime.now()}] processing feature")

    # we have one station that is at the exact same location as another station, so we need to drop one of them
    df = df.groupby(["timestamp", "latitude", "longitude"]).aggregate({
        "aqsid":
        "first",
        "value":
        aggregation_method
    }).reset_index()
    if verbose: print(f"[{datetime.now()}] dataframe shape: {df.shape}")

    # map the h3 index at the leaf resolution to the station
    # pivot the dataframe so that we have a column for each timestamp and a row for each h3 index
    df = df.pivot(index=["latitude", "longitude"], columns="timestamp",
                  values="value").reset_index()
    if verbose:
        print(f"[{datetime.now()}] pivoted dataframe shape: {df.shape}")

    if verbose:
        print(f"[{datetime.now()}] processing resolution {leaf_h3_resolution}")
    df["h3_index"] = df.apply(
        lambda x: h3.geo_to_h3(x.latitude, x.longitude, leaf_h3_resolution),
        axis=1)
    df.drop(columns=["latitude", "longitude"], inplace=True)

    node_features = [
    ]  # tuples of (h3_index, value_t1, ..., value_tn), when concatenated will be shape (num_nodes, num_timestamps)

    # iterate through the h3 indices between the leaf resolution and the coarsest resolution
    for next_h3_resolution in range(leaf_h3_resolution - 1,
                                    min_h3_resolution - 2, -1):
        # ensure that the h3_index is the first column
        col_names = df.columns.tolist()
        col_names.remove("h3_index")
        # sort the columns by timestamp
        col_names.sort()
        col_names.insert(0, "h3_index")
        df = df[col_names]
        # add values for the current resolution
        node_features.extend(df.to_numpy())

        if next_h3_resolution < min_h3_resolution: break
        if verbose:
            print(
                f"[{datetime.now()}] processing resolution {next_h3_resolution}"
            )
        # get the h3 index for each station at the next_resolution
        df["next_h3_index"] = df.apply(
            lambda x: h3.h3_to_parent(x.h3_index, next_h3_resolution), axis=1)
        # group by the next h3 index
        df.drop(columns=["h3_index"], inplace=True)
        df = df.groupby("next_h3_index").aggregate(
            aggregation_method).reset_index()
        # rename the h3 index to the current h3 index
        df = df.rename(columns={"next_h3_index": "h3_index"})

    # add another parent node for the entire graph
    if include_root_node:
        if verbose: print(f"[{datetime.now()}] adding root node")
        root_node_id = "root"
        df.drop(columns=["h3_index"], inplace=True)
        node_features.append(
            np.concatenate((np.array([root_node_id]),
                            df.apply(aggregation_method).values.T)))

    return node_features


def filter_aqsids(
        stations_info: pd.DataFrame,
        remove_aqsid: Union[List[str], None] = ["000000000"],
        aqsid_col_name: str = "aqsid",
        verbose: bool = False,
    ) -> pd.DataFrame:
    """Filter stations based on aqsid."""
    if verbose:
        print(f"Filtering from {len(stations_info)} stations.")

    if remove_aqsid is not None:
        if verbose:
            print(f"Removing stations with aqsid in {remove_aqsid}.")
        stations_info = stations_info[~stations_info[aqsid_col_name].isin(remove_aqsid)]

    if verbose:
        print(f"Returning {len(stations_info)} stations.")  

    return stations_info


def filter_lat_lon(
        stations_info: pd.DataFrame,
        remove_lat_lon: Union[List[Tuple[float, float]], None] = (0, 0),
        lat_col_name: str = "latitude",
        lon_col_name: str = "longitude",
        verbose: bool = False,
    ) -> pd.DataFrame:
    """Filter stations based on lat-lon locations."""
    if verbose:
        print(f"Filtering from {len(stations_info)} stations.")

    if remove_lat_lon is not None:
        if verbose:
            print(f"Removing stations with lat-long paris in {remove_lat_lon}.")
        stations_info = stations_info[
            ~stations_info[[lat_col_name, lon_col_name]].apply(
                lambda x: tuple(x) in remove_lat_lon, axis=1
            )
        ]
    
    if verbose:
        print(f"Returning {len(stations_info)} stations.")  

    return stations_info


def round_station_lat_lon(
        stations_info: pd.DataFrame,
        round_lat_lon: Union[int, None] = 2,
        lat_col_name: str = "latitude",
        lon_col_name: str = "longitude",
        verbose: bool = False,
    ) -> pd.DataFrame:
    """Filter stations based on aqsid."""
    if verbose:
        print(f"Filtering from {len(stations_info)} stations.")

    if round_lat_lon is not None:
        if verbose:
            print(f"Rounding lat and lon to {round_lat_lon} decimal places.")
        stations_info = stations_info.round({lat_col_name: round_lat_lon, lon_col_name: round_lat_lon})
    
    if verbose:
        print(f"Returning {len(stations_info)} stations.")  

    return stations_info


def remove_duplicate_lat_lon(
        df: pd.DataFrame,
        lat_col_name: str = "latitude",
        lon_col_name: str = "longitude",
        verbose: bool = False,
    ) -> pd.DataFrame:
    """Remove duplicate lat-lon pairs."""
    if verbose:
        print(f"Removing duplicates from {len(df)} rows.")

    df = df.drop_duplicates(subset=[lat_col_name, lon_col_name])

    if verbose:
        print(f"Returning {len(df)} rows.")

    return df


def remove_duplicate_aqsid(
        df: pd.DataFrame,
        aqsid_col_name: str = "aqsid",
        verbose: bool = False,
    ) -> pd.DataFrame:
    """Remove duplicate aqsid pairs."""
    if verbose:
        print(f"Removing duplicates from {len(df)} rows.")

    df = df.drop_duplicates(subset=[aqsid_col_name])

    if verbose:
        print(f"Returning {len(df)} rows.")

    return df


def apply_filters(
        df: pd.DataFrame,
        filters: List[Callable],
        verbose: bool = False,
    ) -> pd.DataFrame:
    """Apply a list of filters to a dataframe."""
    for f in filters:
        if verbose:
            print(f"Applying filter {f.__name__}.")
        df = f(df, verbose=verbose)
    return df


