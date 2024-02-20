from datetime import datetime
from typing import List, Union, Callable, Tuple, Dict

import h3
import torch
import numpy as np
import pandas as pd
from torch_geometric.data import Data
from aq_utilities.data import load_hourly_data, load_hourly_feature, load_stations_info

from aq_geometric.data.dataframe import process_feature, apply_filters, filter_aqsids, round_station_lat_lon, filter_lat_lon, remove_duplicate_aqsid, remove_duplicate_lat_lon


def determine_leaf_resolution(
    df: pd.DataFrame,
    min_h3_resolution: int = 0,
    max_h3_resolution: int = 12,
    verbose: bool = False,
) -> int:
    """Determine the leaf resolution that will give us unique hexagons for each station."""
    # we have one station that is at the exact same location as another station, so we need to drop one of them
    assert "latitude" in df.columns and "longitude" in df.columns, "df must have latitude and longitude columns"
    assert "aqsid" in df.columns, "df must have aqsid column"

    df = df.groupby(["latitude", "longitude"]).aggregate({
        "aqsid": "first"
    }).reset_index()

    # find the MAX_H3_RESOLUTION that will give us unique hexagons for each station
    leaf_h3_resolution: int = min_h3_resolution
    if verbose: print(f"[{datetime.now()}] determining leaf resolution")
    for i in range(min_h3_resolution, max_h3_resolution):
        if verbose: print(f"[{datetime.now()}] trying resolution {i}")
        if len(df["aqsid"].values) == len(
                df.apply(lambda x: h3.geo_to_h3(x.latitude, x.longitude, i),
                         axis=1).unique()):
            leaf_h3_resolution = i
            if verbose: print(f"[{datetime.now()}] found resolution {i}")
            break

    return leaf_h3_resolution


def get_edges_from_remote(
    engine: "sqlalchemy.engine.Engine",
    date: str,
    selected_aqsids: Union[List[str], None] = None,
    stations_info_filters: List[Callable] = [
        filter_aqsids,
        round_station_lat_lon,
        filter_lat_lon,
        remove_duplicate_aqsid,
        remove_duplicate_lat_lon,
    ],
    min_h3_resolution: int = 0,
    leaf_h3_resolution: Union[int, None] = None,
    max_h3_resolution: int = 12,
    make_undirected: bool = True,
    include_self_loops: bool = True,
    with_edge_features: bool = True,
    min_to_root_edge_distance: float = 0.0,
    include_root_node: bool = True,
    as_df: bool = True,
    verbose: bool = False,
) -> Union[List[Tuple[int, int]], List[Tuple[int, int, float]], List[Tuple[
        int, int]]]:
    """Get the edges for the graph from remote."""
    # validate the inputs
    assert min_h3_resolution >= 0, "min_h3_resolution must be greater than or equal to 0"
    assert max_h3_resolution <= 15, "max_h3_resolution must be less than or equal to 15"
    assert min_h3_resolution <= max_h3_resolution, "min_h3_resolution must be less than or equal to max_h3_resolution"
    assert leaf_h3_resolution is None or leaf_h3_resolution >= min_h3_resolution, "leaf_h3_resolution must be greater than or equal to min_h3_resolution"
    assert leaf_h3_resolution is None or leaf_h3_resolution <= max_h3_resolution, "leaf_h3_resolution must be less than or equal to max_h3_resolution"
    
    if verbose: print(f"[{datetime.now()}] computing nodes")

    # get the stations info using the aqsid filter if present
    stations_info = load_stations_info(
        engine=engine,
        query_date=date,
        aqsid=selected_aqsids,
        verbose=verbose,
    )

    # apply filters
    stations_info = apply_filters(
        stations_info,
        stations_info_filters,
        verbose=verbose,
    )
    
    # determine the leaf resolution
    leaf_h3_resolution = determine_leaf_resolution(
        df=stations_info,
        min_h3_resolution=min_h3_resolution,
        max_h3_resolution=max_h3_resolution,
        verbose=verbose,
    )

    # obtain edges
    edges = get_edges_from_df(
        df=stations_info,
        min_h3_resolution=min_h3_resolution,
        leaf_h3_resolution=leaf_h3_resolution,
        make_undirected=make_undirected,
        include_self_loops=include_self_loops,
        with_edge_features=with_edge_features,
        include_root_node=include_root_node,
        min_to_root_edge_distance=min_to_root_edge_distance,
        as_df=as_df,
        verbose=verbose,
    )

    return edges


def get_edges_from_df(
    df: pd.DataFrame,
    min_h3_resolution: int,
    leaf_h3_resolution: int,
    make_undirected: bool,
    include_self_loops: bool,
    with_edge_features: bool,
    min_to_root_edge_distance: float = 0.0,
    include_root_node: bool = True,
    as_df: bool = True,
    verbose: bool = False,
) -> Union[List[Tuple[int, int]], List[Tuple[int, int, float]], List[Tuple[
        int, int]]]:
    """Process the edges and edge features for the graph."""
    assert "latitude" in df.columns and "longitude" in df.columns, "df must have latitude and longitude columns"

    # we have one more more stations with the exact same location as another station, so we need to drop one of them
    df = df.copy(deep=True).groupby(["latitude", "longitude"]).aggregate({
        "aqsid": "first"
    }).reset_index()

    if verbose:
        print(f"[{datetime.now()}] processing resolution {leaf_h3_resolution}")
    # map the h3 index at the leaf resolution to the station
    df["h3_index"] = df.apply(
        lambda x: h3.geo_to_h3(x.latitude, x.longitude, leaf_h3_resolution),
        axis=1)

    edges = [
    ]  # tuples of (h3_index1, h3_index2), when concatenated will be shape (2, num_edges)
    edge_attr = [
    ]  # tuples of (h3_index1, h3_index2, distance), when concatenated will be shape (num_edges, 1)
    node_counter = 0  # counter for the node ids

    # iterate through the h3 indices between the leaf resolution and the coarsest resolution
    for next_h3_resolution in range(leaf_h3_resolution - 1,
                                    min_h3_resolution - 2, -1):
        # add edges for the current resolution
        node_counter += len(df["h3_index"].values)
        current_resolution_nodes = set(df["h3_index"].unique().tolist())
        for _, row in df.iterrows():
            # we already have all h3 indices at this resolution, but we need to see if any of them are neighbors
            # get the neighbors of the current h3 index
            neighbors = h3.k_ring(row.h3_index, 1)
            # check if any of the neighbors are in the current resolution. note that k_ring returns the current h3 index as well
            if any([
                    n in current_resolution_nodes for n in neighbors
                    if n != row.h3_index
            ]):
                # add the edges
                for n in neighbors:
                    if n in current_resolution_nodes:
                        if n == row.h3_index and include_self_loops:
                            edges.append((row.h3_index, n))
                            if with_edge_features: edge_attr.append((row.h3_index, n, 0))
                            if make_undirected:
                                edges.append((n, row.h3_index))
                                if with_edge_features: edge_attr.append((row.h3_index, n, 0))
                        elif n != row.h3_index:
                            edges.append((row.h3_index, n))
                            if make_undirected: edges.append((n, row.h3_index))
                            # we need to get lat-lon for the distance calculation
                            if with_edge_features:
                                lat1, lon1 = h3.h3_to_geo(row.h3_index)
                                lat2, lon2 = h3.h3_to_geo(n)
                                distance = h3.point_dist((lat1, lon1),
                                                        (lat2, lon2))
                                edge_attr.append((row.h3_index, n, distance))
                                if make_undirected:
                                    edge_attr.append((n, row.h3_index, distance))

        if next_h3_resolution < min_h3_resolution: break
        if verbose:
            print(
                f"[{datetime.now()}] processing resolution {next_h3_resolution}"
            )
        # get the h3 index for each station at the next_resolution
        df["next_h3_index"] = df.apply(
            lambda x: h3.h3_to_parent(x.h3_index, next_h3_resolution), axis=1)
        # add edges for the next resolution
        edges.extend(df[["h3_index", "next_h3_index"
                         ]].apply(lambda x: (x.h3_index, x.next_h3_index),
                                  axis=1).values)
        if make_undirected:
            edges.extend(df[["h3_index", "next_h3_index"
                             ]].apply(lambda x: (x.next_h3_index, x.h3_index),
                                      axis=1).values)
        if with_edge_features:
            new_edge_attrs = [
                (v[0], v[1],
                 h3.point_dist(h3.h3_to_geo(v[0]), h3.h3_to_geo(v[1])))
                for v in df[["h3_index", "next_h3_index"]].to_numpy()
            ]
            edge_attr.extend(new_edge_attrs)
            if make_undirected:
                edge_attr.extend([(v[1], v[0], v[2]) for v in new_edge_attrs])
        # group by the next h3 index
        df = df.groupby("next_h3_index").aggregate({
            "aqsid": "first"
        }).reset_index()  # we don't need to aggregate the values
        # rename the h3 index to the current h3 index
        df = df.rename(columns={"next_h3_index": "h3_index"})

    # add another parent node for the entire graph if needed
    if include_root_node:
        if verbose: print(f"[{datetime.now()}] adding root node")
        root_node_id = "root"
        edges.extend([(root_node_id, n) for n in df["h3_index"].values])
        if with_edge_features:
            edge_attr.extend([(n, root_node_id, min_to_root_edge_distance)
                              for n in df["h3_index"].values
                              ])  # for now we have 0 for the distance

    if verbose: print(f"[{datetime.now()}] processed {len(edges)} edges")

    # return as a dataframe
    if as_df:
        if with_edge_features:
            return  pd.DataFrame(edge_attr, columns=["from", "to", "distance"])
        else: return pd.DataFrame(edges, columns=["from", "to"])
    # return as a list of tuples
    if with_edge_features:
        assert len(edges) == len(edge_attr)
        return edges, edge_attr
    else:
        return edges


def get_nodes_from_df(
    df: pd.DataFrame,
    min_h3_resolution: int = 0,
    leaf_h3_resolution: int = 9,
    include_root_node: bool = True,
    as_df: bool = True,
    verbose: bool = False,
) -> List[Tuple[Union[str, None], str, int]]:
    """Process the edges and edge features for the graph."""
    assert "latitude" in df.columns and "longitude" in df.columns, "df must have latitude and longitude columns"
    if verbose:
        print(f"[{datetime.now()}] processing resolution {leaf_h3_resolution}")
        print(
            f"[{datetime.now()}] after resolution {leaf_h3_resolution}, we have {len(df)} nodes"
        )
    # map the h3 index at the leaf resolution to the station
    df["h3_index"] = df.apply(
        lambda x: h3.geo_to_h3(x.latitude, x.longitude, leaf_h3_resolution),
        axis=1)
    # store as a dataframe, adding new rows for each resolution
    node_df = df[["aqsid", "h3_index"]].copy(deep=True)

    # the aqsid is not meaningful except at the leaf resolution
    df["aqsid"] = None

    # iterate through the h3 indices between the leaf resolution and the coarsest resolution
    for next_h3_resolution in range(leaf_h3_resolution - 1,
                                    min_h3_resolution - 2, -1):
        if next_h3_resolution < min_h3_resolution: break
        if verbose:
            print(
                f"[{datetime.now()}] processing resolution {next_h3_resolution}"
            )
        # get the h3 index for each station at the next_resolution
        df["next_h3_index"] = df.apply(
            lambda x: h3.h3_to_parent(x.h3_index, next_h3_resolution), axis=1)
        # group by the next h3 index
        df = df.groupby("next_h3_index").aggregate({
            "aqsid": "first"
        }).reset_index()  # we don't need to aggregate the values
        # rename the h3 index to the current h3 index
        df = df.rename(columns={"next_h3_index": "h3_index"})
        # add these new rows to the node_df
        node_df = pd.concat([node_df, df[["aqsid", "h3_index"]]])
        if verbose:
            print(
                f"[{datetime.now()}] after resolution {next_h3_resolution}, we have {len(node_df)} nodes"
            )

    # add another parent node for the entire graph if needed
    if include_root_node:
        if verbose: print(f"[{datetime.now()}] adding root node")
        root_node_id = "root"
        node_df = pd.concat([
            node_df,
            pd.DataFrame({
                "aqsid": [None],
                "h3_index": [root_node_id]
            })
        ])

    # the node id is the index
    node_df["node_id"] = range(len(node_df))
    if verbose: print(f"[{datetime.now()}] processed {len(node_df)} nodes")

    # return as a dataframe
    if as_df:
        return node_df
    # return as a list of tuples
    return node_df.to_numpy()


def get_node_features(
    df: pd.DataFrame,
    nodes: Union[pd.DataFrame, List[Tuple[Union[str, None], str, int]]],
    missing_value: float = -1.0,
    as_df: bool = False,
    verbose: bool = False,
) -> Union[pd.DataFrame, List[np.ndarray]]:
    """Use the nodes to re-index the dataframe.
    
    This may result in nodes with missing values for the features, which are
    filled using the missing_value parameter.

    Args:
        df: pd.DataFrame: the dataframe to re-index
        nodes: pd.DataFrame or List[Tuple[Union[str, None], str, int]]: the nodes
        missing_value: float: the value to fill missing values with

    Returns:
        pd.DataFrame or np.ndarray: the re-indexed dataframe or list of arrays
    """
    # we assume that the dataframe has columns for the aqsid, h3_index and node_id
    # if nodes is an array, it is of shape (num_nodes, 3) with columns (aqsid, h3_index, node_id)
    if verbose: print(f"[{datetime.now()}] re-indexing dataframe")
    if not isinstance(nodes, pd.DataFrame):
        nodes_df = pd.DataFrame(nodes, columns=["aqsid", "h3_index", "node_id"])
    else: nodes_df = nodes.copy(deep=True)

    if verbose: print(f"[{datetime.now()}] nodes_df has shape {nodes_df.shape}")

    # join the dataframes using the h3_index
    nodes_df = nodes_df.merge(df, on="h3_index", how="left").fillna(missing_value)

    if verbose: print(f"[{datetime.now()}] after join nodes_df has shape {nodes_df.shape}")

    # drop the aqsid and h3_index columns
    nodes_df.drop(columns=["aqsid", "h3_index"], inplace=True)
    nodes_df.set_index("node_id", inplace=True)

    if verbose: print(f"[{datetime.now()}] processed dataframe")
    if verbose: print(f"[{datetime.now()}] nodes_df has shape {nodes_df.shape}")

    # return as a dataframe
    if as_df:
        return nodes_df
    # return as a list of arrays
    return nodes_df.values


def load_feature_for_nodes(
    engine: "sqlalchemy.engine.Engine",
    nodes: Union[pd.DataFrame, List[Tuple[Union[str, None], str, int]]],
    feature: str,
    feature_start_time: str,
    feature_end_time: str,
    feature_timestamps: Union[pd.DatetimeIndex, None] = None,
    h3_indices: Union[List[str], None] = None,
) -> List[pd.DataFrame]:
    """Load a feature for the nodes."""
    feature_df = load_hourly_feature(
        engine=engine,
        feature=feature,
        start_time=feature_start_time,
        end_time=feature_end_time,
        h3_indices_filter=h3_indices,
        aqsids_filter=None,
        verbose=True,
    )

    if feature_timestamps is not None and h3_indices is not None:
        feature_df = _ensure_feature_axis(
            feature_df,
            timestamps=feature_timestamps,
            h3_indices=h3_indices,
        )

    feature_df = feature_df.pivot(index="h3_index", columns="timestamp", values="value")

    feature_df = get_node_features(
        df=feature_df,
        nodes=nodes,
        missing_value=np.nan,
        as_df=True,
        verbose=True,
    )
    
    return feature_df


def make_features_for_nodes(
    engine: "sqlalchemy.engine.Engine",
    nodes: Union[pd.DataFrame, List[Tuple[Union[str, None], str, int]]],
    features: List[str],
    start_time: str,
    end_time: str,
    freq: str,
    time_interval_closed: bool = False,
    missing_value: Union[int, float] = -1,
    as_df: bool = True,
    verbose: bool = False,
) -> Union[List[pd.DataFrame], List[np.ndarray]]:
    """Get features for nodes."""
    feature_dfs = []
    timestamps = pd.date_range(start=start_time, end=end_time, freq=freq, inclusive="left" if time_interval_closed == False else "both")
    
    h3_indices = []
    if isinstance(nodes, pd.DataFrame):
        h3_indices = nodes["h3_index"].unique().tolist()
    else:
        h3_indices = [n[1] for n in nodes]

    for feature in features:

        if verbose: print(f"[{datetime.now()}] loading feature {feature}")

        feature_dfs.append(
            load_feature_for_nodes(
                engine=engine,
                nodes=nodes,
                feature=feature,
                feature_start_time=start_time,
                feature_end_time=end_time,
                feature_timestamps=timestamps,
                h3_indices=h3_indices,
            ).fillna(missing_value)
        )

    if as_df:
        return feature_dfs
    else:
        return [df.values for df in feature_dfs]


def get_nodes_from_remote(
    engine: "sqlalchemy.engine.Engine",
    date: str,
    selected_aqsids: Union[List[str], None] = None,
    stations_info_filters: List[Callable] = [
        filter_aqsids,
        round_station_lat_lon,
        filter_lat_lon,
        remove_duplicate_aqsid,
        remove_duplicate_lat_lon,
    ],
    min_h3_resolution: int = 0,
    leaf_h3_resolution: Union[int, None] = None,
    max_h3_resolution: int = 12,
    include_root_node: bool = True,
    verbose: bool = False, 
) -> Union[pd.DataFrame, List[Tuple[Union[str, None], str, int]]]:
    """Get the nodes for the graph from remote."""
    # validate the inputs
    assert min_h3_resolution >= 0, "min_h3_resolution must be greater than or equal to 0"
    assert max_h3_resolution <= 15, "max_h3_resolution must be less than or equal to 15"
    assert min_h3_resolution <= max_h3_resolution, "min_h3_resolution must be less than or equal to max_h3_resolution"
    assert leaf_h3_resolution is None or leaf_h3_resolution >= min_h3_resolution, "leaf_h3_resolution must be greater than or equal to min_h3_resolution"
    assert leaf_h3_resolution is None or leaf_h3_resolution <= max_h3_resolution, "leaf_h3_resolution must be less than or equal to max_h3_resolution"
    
    if verbose: print(f"[{datetime.now()}] computing nodes")

    # get the stations info using the aqsid filter if present
    stations_info = load_stations_info(
        engine=engine,
        query_date=date,
        aqsid=selected_aqsids,
        verbose=verbose,
    )

    # apply filters
    stations_info = apply_filters(
        stations_info,
        stations_info_filters,
        verbose=verbose,
    )
    
    # determine the leaf resolution
    leaf_h3_resolution = determine_leaf_resolution(
        df=stations_info,
        min_h3_resolution=min_h3_resolution,
        max_h3_resolution=max_h3_resolution,
        verbose=verbose,
    )
    
    # obtain nodes
    nodes = get_nodes_from_df(
        df=stations_info,
        min_h3_resolution=min_h3_resolution,
        leaf_h3_resolution=leaf_h3_resolution,
        include_root_node=include_root_node,
        as_df=True,
        verbose=verbose,
    )

    return nodes

def make_graph(
    engine: "sqlalchemy.engine.Engine",
    features: List[str],
    targets: List[str],
    feature_start_time: str,
    feature_end_time: str,
    target_start_time: str,
    target_end_time: str,
    freq: str,
    compute_nodes: bool = True,
    nodes: Union[pd.DataFrame, List[Tuple[Union[str, None], str, int]], None] = None,
    selected_aqsids: Union[List[str], None] = None,
    stations_info_filters: List[Callable] = [
        filter_aqsids,
        round_station_lat_lon,
        filter_lat_lon,
        remove_duplicate_aqsid,
        remove_duplicate_lat_lon,
    ],
    selected_h3_indices: Union[List[str], None] = None,
    min_h3_resolution: int = 0,
    leaf_h3_resolution: Union[int, None] = None,
    max_h3_resolution: int = 12,
    include_root_node: bool = True,
    compute_edges: bool = True,
    edges: Union[np.ndarray, List[Tuple[str, str]], None] = None,
    edge_attr: Union[np.ndarray, List[Tuple[str, str, float]], None] = None,
    make_undirected: bool = True,
    include_self_loops: bool = True,
    with_edge_features: bool = True,
    min_to_root_edge_distance: float = 0.0,
    node_feature_missing_value: float = -1.0,
    normalize_features: bool = False,
    verbose: bool = False,
) -> "pytorch_geometric.data.Data":
    """Get a PyTorch Geometric graph object from feature, target, start, and end times.
    
    Args:
        engine: sqlalchemy.engine.Engine: the database engine
        features: List[str]: the features to pull
        targets: List[str]: the targets to pull
        feature_start_time: str: the start time for the features
        feature_end_time: str: the end time for the features
        target_start_time: str: the start time for the targets
        target_end_time: str: the end time for the targets
        freq: str: the frequency for the features and targets
        compute_nodes: bool: whether to compute the nodes
        nodes: pd.DataFrame or List[Tuple[Union[str, None], str, int]]: the nodes
        selected_aqsids: List[str]: the aqsids to include
        stations_info_filters: List[Callable]: the filters to apply to the stations info
        selected_h3_indices: List[str]: the h3 indices to include
        min_h3_resolution: int: the minimum h3 resolution
        leaf_h3_resolution: int: the leaf h3 resolution
        max_h3_resolution: int: the maximum h3 resolution
        include_root_node: bool: whether to include a root node
        compute_edges: bool: whether to compute the edges
        edges: np.ndarray: (2, num_edges) array of (node_id1, node_id2)
        edge_attr: np.ndarray: (num_edges, num_edge_features) array of edge features
        make_undirected: bool: whether to make the edges undirected
        include_self_loops: bool: whether to include self loops
        with_edge_features: bool: whether to include edge features
        min_to_root_edge_distance: float: the distance from the root node
        node_feature_missing_value: float: the value to fill missing node features with
        normalize_features: bool: whether to normalize the features
        verbose: bool: whether to print verbose output
       
    Returns:
        pytorch_geometric.data.Data: the graph data object
    """

    # validate the inputs
    assert len(features) > 0, "features must have at least one element"
    assert len(targets) > 0, "targets must have at least one element"
    assert feature_start_time < feature_end_time, "feature_start_time must be less than feature_end_time"
    assert target_start_time < target_end_time, "target_start_time must be less than target_end_time"
    assert freq in ["1H", "1D", "1W", "1M"], "freq must be one of '1H', '1D', '1W', '1M'"
    assert min_h3_resolution >= 0, "min_h3_resolution must be greater than or equal to 0"
    assert max_h3_resolution <= 15, "max_h3_resolution must be less than or equal to 15"
    assert min_h3_resolution <= max_h3_resolution, "min_h3_resolution must be less than or equal to max_h3_resolution"
    assert leaf_h3_resolution is None or leaf_h3_resolution >= min_h3_resolution, "leaf_h3_resolution must be greater than or equal to min_h3_resolution"
    assert leaf_h3_resolution is None or leaf_h3_resolution <= max_h3_resolution, "leaf_h3_resolution must be less than or equal to max_h3_resolution"
    if compute_edges == False:
        assert edges is not None, "edges must be provided if compute_edges is False"
        if with_edge_features:
            assert edge_attr is not None, "edge_attr must be provided if compute_edges is False and with_edge_features is True"
            assert len(edges) == len(edge_attr), "edges and edge_attr must have the same length"
    if compute_nodes == False:
        assert nodes is not None, "nodes must be provided if compute_nodes is False"
    if selected_aqsids is not None:
        assert len(selected_aqsids) > 0, "selected_aqsids must have at least one element if provided"
    if selected_h3_indices is not None:
        assert len(selected_h3_indices) > 0, "selected_h3_indices must have at least one element if provided"

    if verbose: print(f"[{datetime.now()}] computing graph")

    if compute_nodes:
        # get the stations info using the aqsid filter if present
        stations_info = load_stations_info(
            engine=engine,
            query_date=feature_start_time,
            aqsid=selected_aqsids,
            verbose=verbose,
        )

        # apply filters
        stations_info = apply_filters(
            stations_info,
            stations_info_filters,
            verbose=verbose,
        )
        
        # determine the leaf resolution
        leaf_h3_resolution = determine_leaf_resolution(
            df=stations_info,
            min_h3_resolution=min_h3_resolution,
            max_h3_resolution=max_h3_resolution,
            verbose=verbose,
        )
        
        # obtain nodes
        nodes = get_nodes_from_df(
            df=stations_info,
            min_h3_resolution=min_h3_resolution,
            leaf_h3_resolution=leaf_h3_resolution,
            include_root_node=include_root_node,
            as_df=True,
            verbose=verbose,
        )
    
    if len(nodes) == 0:
        raise ValueError("No nodes were found")
    
    # down-select to only the selected h3 indices if needed
    if selected_h3_indices is not None:
        stations_info = nodes[nodes["h3_index"].isin(selected_h3_indices)]
        if verbose:
            print(f"[{datetime.now()}] down-selected to {len(nodes)} stations")
            print(f"[{datetime.now()}] {len(set(nodes['h3_index'].values))} h3 indices of the {len(set(selected_h3_indices))} h3 indices matched")
    if len(nodes) == 0:
        raise ValueError("No nodes were found")
    
    # obtain edges and edge attr
    if compute_edges:
        edges_with_attr_df = get_edges_from_df(
            df=stations_info,
            min_h3_resolution=min_h3_resolution,
            leaf_h3_resolution=leaf_h3_resolution,
            min_to_root_edge_distance=min_to_root_edge_distance,
            make_undirected=make_undirected,
            include_self_loops=include_self_loops,
            verbose=verbose,
            with_edge_features=with_edge_features,
            as_df=True,
        )
    else:
        # if edges is a dataframe, it is of shape (num_edges, 2) with columns (from, to)
        # if edge_attr is a dataframe, it is of shape (num_edges, num_edge_features) with columns (from, to, ...)
        if isinstance(edges, pd.DataFrame):
            edges_with_attr_df = edges
        else:
            edges_with_attr_df = pd.DataFrame({
                "from": edges[:, 0],
                "to": edges[:, 1],
            })
        if with_edge_features:
            if isinstance(edge_attr, pd.DataFrame):
                edges_with_attr_df = edges_with_attr_df.merge(edge_attr, on=["from", "to"], how="left")
            else:
                edge_attr_df = pd.DataFrame(edge_attr, columns=["from", "to"] + [f"feature_{i}" for i in range(edge_attr.shape[1] - 2)])
                edges_with_attr_df = edges_with_attr_df.merge(edge_attr_df, on=["from", "to"], how="left")

    # prepare to pull features and targets
    feature_dfs = make_features_for_nodes(
        engine=engine,
        nodes=nodes,
        features=features,
        start_time=feature_start_time,
        end_time=feature_end_time,
        freq=freq,
        time_interval_closed=False,
        missing_value=np.nan,
        verbose=verbose,
    )
    target_dfs = make_features_for_nodes(
        engine=engine,
        nodes=nodes,
        features=targets,
        start_time=target_start_time,
        end_time=target_end_time,
        freq=freq,
        time_interval_closed=False,
        missing_value=np.nan,
        verbose=verbose,
    )

    # make the graph
    graph = make_graph_from_features(
        nodes=nodes,
        node_features=feature_dfs,
        node_targets=target_dfs,
        edges=edges_with_attr_df[["from", "to"]].values,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        target_start_time=target_start_time,
        target_end_time=target_end_time,
        edge_attr=edges_with_attr_df.values if with_edge_features else None,
        normalize_features=normalize_features,
        missing_value=node_feature_missing_value,
        verbose=verbose,
    )

    return graph


def make_graph_from_features(
        nodes: Union[pd.DataFrame, List[Tuple[Union[str, None], str, int]]],
        node_features: List[np.ndarray],
        node_targets: List[np.ndarray],
        edges: Union[np.ndarray, List[Tuple[str, str]]],
        feature_start_time: str,
        feature_end_time: str,
        target_start_time: str,
        target_end_time: str,
        edge_attr: Union[np.ndarray, List[Tuple[str, str, float]], None] = None,
        normalize_features: bool = False,
        missing_value: float = np.nan,
        verbose: bool = False,
) -> "pytorch_geometric.data.Data":
    """Get a PyTorch Geometric graph object from nodes, edges, and features.
    
    Args:
        nodes: pd.DataFrame or List[Tuple[Union[str, None], str, int]]: the nodes
        edges: np.ndarray: (2, num_edges) array of (node_id1, node_id2)
        node_features: np.ndarray: (num_nodes, num_features) array of node features
        node_targets: np.ndarray: (num_nodes, num_targets) array of node targets
        feature_start_time: str: the start time for the features
        feature_end_time: str: the end time for the features
        target_start_time: str: the start time for the targets
        target_end_time: str: the end time for the targets
        edge_attr: np.ndarray: (num_edges, num_edge_features) array of edge features
        verbose: bool: whether to print debug information

    Returns:
        pytorch_geometric.data.Data: the graph data object
    """

    # validate
    assert all([len(n) == len(nodes) for n in node_features])
    assert all([len(n) == len(nodes) for n in node_targets])
    assert len(edges) == len(edge_attr) if edge_attr is not None else True

    h3_index_to_id_map = {v[1]: v[2] for v in nodes.to_numpy()}
    # we need to map the edges from h3 index to node id
    edges = np.array([(h3_index_to_id_map[e[0]], h3_index_to_id_map[e[1]])
                        for e in edges]).T
    # we might need to do the same for edge_attr if provided
    if edge_attr is not None:
        edge_attr = np.array([e[2] for e in edge_attr], ndmin=2).T

    # the node features have already been re-indexed, so we can cancatenate them
    node_features = np.concatenate(node_features, axis=1)
    node_targets = np.concatenate(node_targets, axis=1)

    # we want the values to be in np.float16
    node_features = node_features.astype(np.float16)
    node_targets = node_targets.astype(np.float16)

    # normalize the features if needed
    if normalize_features:
        # compute the std for each row
        node_std = np.nanstd(node_features, axis=1)
        # compute the mean for each row
        node_mean = np.nanmean(node_features, axis=1)
        # normalize the features if the std is not 0
        node_features = np.where(node_std != 0,
                                (node_features - node_mean) / node_std,
                                node_features)
        # where the std is 0, we set the value to 0
        node_features = np.where(node_std == 0, missing_value, node_features)
    
    # we need to handle missing values
    node_features = np.nan_to_num(node_features, nan=missing_value)
    node_targets = np.nan_to_num(node_targets, nan=missing_value)

    # we need to handle missing values (negative 1 or np.nan) with a mask
    node_features_mask = torch.tensor(node_features >= 0, dtype=torch.bool)
    node_targets_mask = torch.tensor(node_targets >= 0, dtype=torch.bool)
    # combine the masks for an overall missingness mask
    valid_measurement_mask = torch.concat([node_features_mask, node_targets_mask], dim=1)
    # for each node mask for all features and targets being valid
    node_all_valid_measurements_mask = torch.all(valid_measurement_mask, dim=1)

    if verbose: print(f"[{datetime.now()}] node_feature_mask has shape {node_features_mask.shape}")
    if verbose: print(f"[{datetime.now()}] node_targets_mask has shape {node_targets_mask.shape}")
    if verbose: print(f"[{datetime.now()}] valid_measurement_mask has shape {valid_measurement_mask.shape}")
    if verbose: print(f"[{datetime.now()}] node_all_valid_measurements_mask has shape {node_all_valid_measurements_mask.shape}")
    
    edge_node_all_valid_measurements_mask = torch.logical_and(
        node_all_valid_measurements_mask[edges[0]], node_all_valid_measurements_mask[edges[1]])

    if verbose: print(f"[{datetime.now()}] edge_node_all_valid_measurements_mask has shape {edge_node_all_valid_measurements_mask.shape}")

    if verbose: print(f"[{datetime.now()}] processed masks")

    # make the graph data object
    data = Data(
        x=torch.tensor(node_features, dtype=torch.float),
        y=torch.tensor(node_targets, dtype=torch.float),
        edge_index=torch.tensor(edges, dtype=torch.long),
        edge_attr=torch.tensor(edge_attr, dtype=torch.float),
        valid_measurement_mask=valid_measurement_mask,
        node_all_valid_measurements_mask=node_all_valid_measurements_mask,
        edge_node_all_valid_measurements_mask=edge_node_all_valid_measurements_mask,
        node_features_mask=node_features_mask,
        node_targets_mask=node_targets_mask,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        target_start_time=target_start_time,
        target_end_time=target_end_time,
    )
    data.validate()

    return data


def process_graph(
    features_df: Union[pd.DataFrame, List[pd.DataFrame]],
    targets_df: Union[pd.DataFrame, List[pd.DataFrame]],
    feature_start_time: str,
    feature_end_time: str,
    target_start_time: str,
    target_end_time: str,
    aggregation_method: Union[Callable, str] = "mean",
    min_h3_resolution: int = 0,
    leaf_h3_resolution: Union[int, None] = None,
    max_h3_resolution: int = 12,
    compute_edges: bool = True,
    make_undirected: bool = True,
    with_edge_features: bool = True,
    min_to_root_edge_distance: float = 0.0,
    include_root_node: bool = True,
    return_h3_index_to_node_id_map: bool = False,
    return_h3_index_to_aqsid_map: bool = False,
    processed_edges: Union[Tuple[List[Tuple[str, str]],
                                 List[Tuple[str, str, float]]], None] = None,
    verbose: bool = False,
) -> Union["pytorch_geometric.data.Data", Tuple["pytorch_geometric.data.Data",
                                                Dict[str, int]]]:
    """Take feature and target DataFrames and process them into a graph Data object."""
    if isinstance(features_df, pd.DataFrame):
        features_df = [features_df]
    if isinstance(targets_df, pd.DataFrame):
        targets_df = [targets_df]

    # iterate through features and targets dataframes
    for df in features_df + targets_df:
        assert "latitude" in df.columns and "longitude" in df.columns, "df must have latitude and longitude columns"
        assert "aqsid" in df.columns, "df must have aqsid column"
        assert "value" in df.columns, "df must have value column"
        assert "timestamp" in df.columns, "df must have timestamp column"
        # check that the shapes are the same
        assert df.shape == features_df[
            0].shape, "all dataframes must have the same shape"

    if verbose: print(f"[{datetime.now()}] processing graph")

    # get the leaf resolution that will give us unique hexagons for each station
    if leaf_h3_resolution is None:
        leaf_h3_resolution = determine_leaf_resolution(features_df[0],
                                                       min_h3_resolution,
                                                       max_h3_resolution,
                                                       verbose=verbose)
    if verbose:
        print(f"[{datetime.now()}] leaf resolution: {leaf_h3_resolution}")

    # process the edges and edge features
    if compute_edges:
        edges, edge_attr = get_edges_from_df(
            features_df[0], min_h3_resolution, leaf_h3_resolution,
            make_undirected, with_edge_features,
            min_to_root_edge_distance=min_to_root_edge_distance,
            include_root_node=include_root_node, verbose=verbose)
    else:
        assert processed_edges is not None, "if compute_edges is False, then processed_edges must be provided"
        edges, edge_attr = processed_edges

    if verbose: print(f"[{datetime.now()}] processed edges")

    # process the features and targets
    node_features = []
    node_targets = []
    # process the features
    for df in features_df:
        node_features.append(
            process_feature(df, feature_start_time, feature_end_time,
                            aggregation_method, min_h3_resolution,
                            leaf_h3_resolution, include_root_node,
                            verbose=verbose))
    for df in targets_df:
        node_targets.append(
            process_feature(df, target_start_time, target_end_time,
                            aggregation_method, min_h3_resolution,
                            leaf_h3_resolution, include_root_node,
                            verbose=verbose))

    if verbose: print(f"[{datetime.now()}] processed features and targets")

    # validate
    assert all([len(n) == len(node_features[0]) for n in node_features])
    assert all([len(n) == len(node_targets[0]) for n in node_targets])
    assert len(node_features[0]) == len(node_targets[0])
    assert len(edges) == len(edge_attr)
    assert all([
        n[0] == t[0] for n, t in zip(node_features[0], node_targets[0])
    ])  # make sure the node ids are the same for the nodes and targets

    # map from h3 index to node id
    h3_index_to_id_map = {v[0]: i for i, v in enumerate(node_features[0])}
    # obtain a mapping from h3 index to aqsid if needed
    h3_index_to_aqsid_map = {}
    if return_h3_index_to_aqsid_map:
        aqsid_to_h3_df = features_df[0][[
            "aqsid", "latitude", "longitude"
        ]].groupby("aqsid").first().reset_index()
        aqsid_to_h3_df["h3_index"] = aqsid_to_h3_df.apply(
            lambda x: h3.geo_to_h3(x.latitude, x.longitude, leaf_h3_resolution
                                   ), axis=1)
        h3_index_to_aqsid_map = {
            v[0]: v[1]
            for v in aqsid_to_h3_df[["h3_index", "aqsid"]].to_numpy()
        }

    if verbose: print(f"[{datetime.now()}] processed maps")

    # we can just remove the h3 index column from the nodes and targets
    node_features = np.stack(
        [v[1:].astype(np.float16) for f in node_features for v in f])
    node_targets = np.stack(
        [v[1:].astype(np.float16) for f in node_targets for v in f])

    # we need to handle missing values (negative 1) with a mask
    node_features_mask = torch.tensor(node_features >= 0, dtype=torch.bool)
    node_targets_mask = torch.tensor(node_targets >= 0, dtype=torch.bool)
    # combine the masks for an overall missingness mask
    valid_measurement_mask = torch.logical_and(node_features_mask,
                                               node_targets_mask)

    # map the edges from h3 index to node id
    edges = np.array([(h3_index_to_id_map[e[0]], h3_index_to_id_map[e[1]])
                      for e in edges]).T
    # map the edge attr from h3 index to node id
    edge_attr = np.array([e[2] for e in edge_attr], ndmin=2).T
    # make a mask for edges based on the missingness mask for the nodes

    valid_measurement_mask_edges = torch.logical_and(
        valid_measurement_mask[edges[0]], valid_measurement_mask[edges[1]])

    if verbose: print(f"[{datetime.now()}] processed masks")

    # make the graph data object
    data = Data(
        x=torch.tensor(node_features, dtype=torch.float),
        y=torch.tensor(node_targets, dtype=torch.float),
        edge_index=torch.tensor(edges, dtype=torch.long),
        edge_attr=torch.tensor(edge_attr, dtype=torch.float),
        valid_measurement_mask=valid_measurement_mask,
        valid_measurement_mask_edges=valid_measurement_mask_edges,
        node_features_mask=node_features_mask,
        node_targets_mask=node_targets_mask,
        feature_start_time=feature_start_time,
        feature_end_time=feature_end_time,
        target_start_time=target_start_time,
        target_end_time=target_end_time,
    )
    data.validate()

    if verbose: print(f"[{datetime.now()}] validated graph")

    response = [data]

    if return_h3_index_to_node_id_map:
        response.append(h3_index_to_id_map)
    if return_h3_index_to_aqsid_map:
        response.append(h3_index_to_aqsid_map)

    return response


def _ensure_feature_axis(
        df: pd.DataFrame,
        h3_indices: List[str],
        timestamps: Union[List[Union[str, datetime]], pd.DatetimeIndex],
        timestamp_col_name: str = "timestamp",
        h3_index_col_name: str = "h3_index",
        values_col_name: str = "value",
) -> pd.DataFrame:
    """Ensure the return from remote has the correct columns and rows."""
    df[timestamp_col_name] = pd.to_datetime(df[timestamp_col_name])
    df = df.pivot(index=timestamp_col_name, columns=h3_index_col_name, values=values_col_name).reindex(index=timestamps, columns=h3_indices)
    df = df.reset_index()
    df = df.rename(columns={"index": timestamp_col_name})
    df = df.melt(id_vars=timestamp_col_name, value_vars=h3_indices, var_name=h3_index_col_name, value_name=values_col_name)
    return df
