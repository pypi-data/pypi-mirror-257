import os
import os.path as osp
from datetime import datetime
from typing import Tuple, List, Union, Callable

import torch
import pandas as pd
from torch_geometric.data import Dataset, Data
from aq_utilities.engine.psql import get_engine
from aq_utilities.data import determine_leaf_h3_resolution
from aq_utilities.data import load_stations_info

from aq_geometric.data import get_nodes_from_remote, get_nodes_from_df, get_edges_from_df, get_edges_from_remote, make_graph, apply_filters, filter_aqsids, round_station_lat_lon, filter_lat_lon, remove_duplicate_aqsid, remove_duplicate_lat_lon 


class AqGeometricDataset(Dataset):
    r"""The AQ Graph dataset from the database.

    Args:
        root (string): Root directory where the dataset should be saved.
        engine (string, optional): SQLAlchemy connection string.
        transform (callable, optional): A function/transform that takes in an
            :obj:`torch_geometric.data.Data` object and returns a transformed
            version. The data object will be transformed before every access.
            (default: :obj:`None`)
        pre_transform (callable, optional): A function/transform that takes in
            an :obj:`torch_geometric.data.Data` object and returns a
            transformed version. The data object will be transformed before
            being saved to disk. (default: :obj:`None`)
        start_time (string, optional): Start time for the features.
        end_time (string, optional): End time for the features.
        sample_freq (string, optional): Sample frequency for the features.
        aqsids (list, optional): List of AQSIDs to include in the dataset.
        features (list): List of features to include in the dataset.
        targets (list): List of targets to include in the dataset.
        time_closed_interval (bool): Whether the time interval is closed.
        samples_in_node_feature (int): Number of samples in the node feature.
        samples_in_node_target (int): Number of samples in the node target.
        aggregation_method (callable, optional): Aggregation method for the features.
            default is :obj:`lambda x: np.mean(x[x >= 0]) if len(x[x >= 0]) > 0 else -1`.
        nan_value (float): Value to use for missing measurements.
        min_h3_resolution (int): Minimum H3 resolution default is 0.
        max_h3_resolution (int): Maximum H3 resolution default is 12.
        include_root_node (bool): Whether to include the root node.
        include_self_loops (bool): Whether to include self loops.
        make_undirected (bool): Whether to make the edges undirected.
        with_edge_features (bool): Whether to compute edge features.
        min_to_root_edge_distance (float): Distance for the edge to the root node.
        verbose (bool): Whether to print verbose output.
    """
    def __init__(
        self,
        root,
        engine = None,
        engine_kwargs: dict = {},
        transform: Union[Callable, None] = None,
        pre_transform: Union[Callable, None] = None,
        pre_filter: Union[Callable, None] = None,
        start_time: str = "2020-01-01",
        end_time: str = "2024-01-01",
        sample_freq: str = "1H",
        aqsids: Union[List[str], None] = None,
        stations_info_filters: List[Callable] = [
            filter_aqsids,
            round_station_lat_lon,
            filter_lat_lon,
            remove_duplicate_aqsid,
            remove_duplicate_lat_lon,
        ],
        features: List[str] = ["PM2.5"],
        targets: List[str] = ["PM2.5"],
        time_closed_interval: bool = False,
        samples_in_node_feature: int = 8,
        samples_in_node_target: int = 1,
        max_samples_in_graph: int = 2880,
        nan_value: float = -1,
        min_h3_resolution: int = 0,
        max_h3_resolution: int = 12,
        include_root_node: bool = True,
        include_self_loops: bool = True,
        make_undirected: bool = True,
        with_edge_features: bool = True,
        min_to_root_edge_distance: float = 0.0,
        verbose: bool = False,
    ):
        if engine is None:
            engine = get_engine(**engine_kwargs)
        self.engine = engine
        self.start_time = start_time
        self.end_time = end_time
        self.sample_freq = sample_freq
        self.aqsids = aqsids
        self.stations_info_filters = stations_info_filters
        self.features = features
        self.targets = targets
        self.time_closed_interval = time_closed_interval
        self.samples_in_node_feature = samples_in_node_feature
        self.samples_in_node_target = samples_in_node_target
        self.max_samples_in_graph = max_samples_in_graph
        self.nan_value = nan_value
        self.min_h3_resolution = min_h3_resolution
        self.max_h3_resolution = max_h3_resolution
        self.include_root_node = include_root_node
        self.make_undirected = make_undirected
        self.include_self_loops = include_self_loops
        self.with_edge_features = with_edge_features
        self.min_to_root_edge_distance = min_to_root_edge_distance
        self.verbose = verbose
        self.graph_index_ranges = []
        self.current_graph_index = 0
        self.current_graph_data = None

        # obtain the timestamps for the features and targets
        self.timestamps = pd.date_range(start=self.start_time,
                                   end=self.end_time,
                                   freq=self.sample_freq,
                                   inclusive="left" if self.time_closed_interval == False else "both")
        # save the length as the number of time steps minus the number of samples in the node feature minus the number of samples in the node target
        self.num_graphs = 1 + len(self.timestamps) - self.samples_in_node_feature - self.samples_in_node_target
    
        super().__init__(root, transform, pre_transform, pre_filter)

        # override the __getitem__ method
        self.__getitem__ = self.__sharded_getitem__


    @property
    def raw_file_names(self) -> List[str]:
        """Return the raw file name of the data and stations info."""
        print(f"{type(self).__name__} does not use raw file names.")
        return []

    @property
    def processed_file_names(self) -> List[str]:
        """Return the processed file names."""
        from glob import glob
        return [
            osp.basename(f)
            for f in glob(osp.join(self.processed_dir, "data_*.pt"))
        ]

    def clear(self):
        """Clear the raw and processed directories."""
        import shutil
        shutil.rmtree(self.processed_dir)
        return None

    def download(self):
        """Query remote database for the data and stations info, saving to csv files."""
        print(f"{type(self).__name__} does not download raw data to disk.")
        return None

    def process(self):
        """Process the data and stations info into individual graphs."""
        # ensure the processed directory exists
        if not osp.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        # check if the there are already processed files
        if len(self.processed_file_names) > 0:
            print(f"Processed files already exist in {self.processed_dir}")
            return
        
        # determine the number of samples allowed in each graph based on the max size
        total_samples = self.samples_in_node_feature + self.samples_in_node_target
        num_samples_in_graph = self.max_samples_in_graph // total_samples
        if self.verbose:
            print(f"max samples in graph: {self.max_samples_in_graph}")
            print(f"num samples in graph: {num_samples_in_graph}")

        # obtain the timestamps for the features and targets
        timestamps = self.timestamps
        # assert that the number of samples in the node feature and target is less than the total number of samples
        assert self.samples_in_node_feature + self.samples_in_node_target <= len(timestamps), "The number of samples in the node feature and target must be less than the total number of samples."
        
        # approach: we want to pull as much data as possible for each graph saved to disk and compute the specific graph dynamically
        # we have two cases, either the data is small enough for one graph or it is not
        # if we can fit all the data into one graph, we will do so
        # if we cannot, we will pull the data for each graph and compute the graph dynamically
        if num_samples_in_graph >= len(timestamps):
            start_times = [timestamps[0]]
            end_times = [timestamps[-1] + pd.Timedelta(self.sample_freq)]  # add one more sample to the end time
        else:
            start_times = timestamps[::num_samples_in_graph].to_list()
            end_times = timestamps[num_samples_in_graph::num_samples_in_graph].to_list()
            start_times.append(end_times[-1])
            end_times.append(pd.to_datetime(timestamps[-1]) + pd.Timedelta(self.sample_freq))  # add one more sample to the end time
        if self.verbose:
            print(f"timestamps: {timestamps}")
            print(f"start times: {start_times}")
            print(f"end times: {end_times}")
        time_idx = 0

        for i, (start_time, end_time) in enumerate(zip(start_times, end_times)):
            # for the first graph, we need to get the nodes and edges, as well as the h3_index_to_node_id_map and h3_index_to_aqsid_map
            if i == 0:
                stations_info = load_stations_info(
                    engine=self.engine,
                    query_date=start_time.strftime("%Y-%m-%d"),
                    aqsid=self.aqsids,
                    verbose=self.verbose,
                )

                # apply filters
                stations_info = apply_filters(
                    stations_info,
                    self.stations_info_filters,
                    verbose=self.verbose,
                )

                # determine the leaf resolution
                leaf_resolution = determine_leaf_h3_resolution(
                    df=stations_info,
                    min_h3_resolution=self.min_h3_resolution,
                    max_h3_resolution=self.max_h3_resolution,
                    verbose=self.verbose,
                )

                # get the h3_index_to_node_id_map and h3_index_to_aqsid_map
                nodes = get_nodes_from_df(
                    df=stations_info,
                    min_h3_resolution=self.min_h3_resolution,
                    leaf_h3_resolution=leaf_resolution,
                    include_root_node=self.include_root_node,
                    verbose=self.verbose,
                )
                h3_index_to_aqsid_map = {k:v for k, v in nodes[["h3_index", "aqsid"]].values}
                h3_index_to_node_id_map = {k:v for k, v in nodes[["h3_index", "node_id"]].values}

                # save the h3_index_to_id_map if one does not exist
                if not osp.exists(
                        osp.join(self.processed_dir,
                                "h3_index_to_node_id_map.pt")):
                    torch.save(
                        h3_index_to_node_id_map,
                        osp.join(self.processed_dir, "h3_index_to_node_id_map.pt"))
                # do the same for the h3_index_to_aqsid_map
                if not osp.exists(
                        osp.join(self.processed_dir, "h3_index_to_aqsid_map.pt")):
                    torch.save(
                        h3_index_to_aqsid_map,
                        osp.join(self.processed_dir, "h3_index_to_aqsid_map.pt"))
                
                # get the edges and edge attributes
                edges_with_features = get_edges_from_df(
                    df=stations_info,
                    min_h3_resolution=self.min_h3_resolution,
                    leaf_h3_resolution=leaf_resolution,
                    make_undirected=self.make_undirected,
                    include_self_loops=self.include_self_loops,
                    with_edge_features=self.with_edge_features,
                    include_root_node=self.include_root_node,
                    min_to_root_edge_distance=self.min_to_root_edge_distance,
                    as_df=True,
                    verbose=self.verbose,
                )
            # for the rest of the graphs, we can use the nodes and edges from the first graph
            graph = make_graph(
                engine=self.engine,
                features=self.features,
                targets=self.targets,
                feature_start_time=start_time,
                feature_end_time=end_time,
                target_start_time=start_time,
                target_end_time=end_time,
                freq=self.sample_freq,
                compute_nodes=False,
                nodes=nodes,
                compute_edges=False,
                edges=edges_with_features,
                edge_attr=edges_with_features,
                verbose=self.verbose,
            )
            if self.verbose:
                print(f"Processed graph {i+1} of {len(end_times)}")
            if self.verbose:
                print(
                    f"Graph start time {start_time}, end time {end_time}."
                )

            if self.pre_transform is not None:
                graph = self.pre_transform(graph)

            # when saving the graph, in the single-file case we want the end index to be the number of timestamps
            torch.save(graph, osp.join(self.processed_dir, f'data_{time_idx}-{min(time_idx+num_samples_in_graph, len(timestamps))}.pt'))
            self.graph_index_ranges.append((time_idx, min(time_idx+num_samples_in_graph, len(timestamps))))
            time_idx += num_samples_in_graph
        print(f"Finished processing {len(end_times)} graphs.")

    def len(self):
        return self.num_graphs
    
    def get(self, idx):
        # ensure we have the graph index ranges
        # get the processed file names
        if self.graph_index_ranges is None or len(self.graph_index_ranges) == 0:
            self.graph_index_ranges = [
                (int(f.split("_")[-1].split("-")[0]), int(f.split("_")[-1].split("-")[1].split(".")[0]))
                for f in self.processed_file_names
            ]
        self.current_graph_index = 0
        if self.verbose:
            print(f"[{datetime.now()}] Getting graph {idx} of {self.num_graphs}")
            print(f"[{datetime.now()}] graph index ranges: {self.graph_index_ranges}")
            print(f"[{datetime.now()}] current graph index: {self.current_graph_index}")
        return self.__sharded_getitem__(idx)

    def __sharded_getitem__(self, idx):
        """Compute the graph for index idx using data from disk."""
        # determine which graph on disk has index idx
        cur_range = self.graph_index_ranges[self.current_graph_index]
        
        # check if there is no overlap
        if idx < cur_range[0] or idx >= cur_range[1] or self.current_graph_data is None:
            for i, (start, end) in enumerate(self.graph_index_ranges):
                if idx >= start and idx < end:
                    # update the current graph index
                    self.current_graph_index = i
                    # load the graph from disk
                    self._load_next_graph()
                    break

        if self.current_graph_data is None:
            raise ValueError(f"Could not load graph from disk which contains index {idx}.")

        # get the data for this range
        time_index_start = idx
        time_index_end = idx + self.samples_in_node_feature + self.samples_in_node_target
        current_graph_index_start = self.graph_index_ranges[self.current_graph_index][0]
        current_graph_index_end = self.graph_index_ranges[self.current_graph_index][1]

        data = self._load_data_from_memory(time_index_start, time_index_end, current_graph_index_start, current_graph_index_end)

        if self.transform is not None:
            data = self.transform(data)

        return data
    

    def _load_next_graph(self) -> None:
        """Load the next graph from disk."""
        # get the file names for the current and next graph
        current_start, current_end = self.graph_index_ranges[self.current_graph_index]
        if self.verbose: print(f"Loading next graph from {current_start} to {current_end}")
        g1 = self._load_graph(current_start, current_end)
        if self.verbose: print(f"Loaded graph {g1}")
        if self.current_graph_index+1 < len(self.graph_index_ranges):
            next_start, next_end = self.graph_index_ranges[self.current_graph_index+1]
            if self.verbose: print(f"Loading next graph from {next_start} to {next_end}")
            g2 = self._load_graph(next_start, next_end)
            if self.verbose: print(f"Loaded graph {g2}")
            # concatinate the graphs
            node_features = torch.cat((g1.x, g2.x), dim=1)
            node_targets = torch.cat((g1.y, g2.y), dim=1)
            node_features_mask = torch.cat((g1.node_features_mask, g2.node_features_mask), dim=1)
            node_targets_mask = torch.cat((g1.node_targets_mask, g2.node_targets_mask), dim=1)
            valid_measurement_mask = torch.cat((g1.valid_measurement_mask, g2.valid_measurement_mask), dim=1)
            feature_start_time = g1.feature_start_time
            feature_end_time = g2.feature_end_time
            target_start_time = g1.target_start_time
            target_end_time = g2.target_end_time
        else:
            # we are at the end of the graph index ranges
            node_features = g1.x
            node_targets = g1.y
            node_features_mask = g1.node_features_mask
            node_targets_mask = g1.node_targets_mask
            valid_measurement_mask = g1.valid_measurement_mask
            feature_start_time = g1.feature_start_time
            feature_end_time = g1.feature_end_time
            target_start_time = g1.target_start_time
            target_end_time = g1.target_end_time

        data = Data(
            x=node_features,
            y=node_targets,
            edge_index=g1.edge_index,
            edge_attr=g1.edge_attr,
            valid_measurement_mask=valid_measurement_mask,
            node_features_mask=node_features_mask,
            node_targets_mask=node_targets_mask,
            feature_start_time=feature_start_time,
            feature_end_time=feature_end_time,
            target_start_time=target_start_time,
            target_end_time=target_end_time,
        )
        data.validate()

        self.current_graph_data = data


    def _load_graph(
            self,
            start: int,
            end: int,
        ) -> Data:
        """Load the graph from disk using start and end indicies."""
        # data is a PyG Data object
        return torch.load(osp.join(self.processed_dir, f'data_{start}-{end}.pt'))


    def _load_data_from_memory(
            self,
            time_index_start: int,
            time_index_end: int,
            current_graph_index_start: int,
            current_graph_index_end: int
        ) -> Data:
        """Load some or all of the graph from memory."""
        # we static edge_index and edge_attr
        edge_index = self.current_graph_data.edge_index
        edge_attr = self.current_graph_data.edge_attr

        # we need to compute the feature and target start and end times
        feature_start_time = pd.to_datetime(self.current_graph_data.feature_start_time) + pd.Timedelta(self.sample_freq) * (time_index_start-current_graph_index_start)
        feature_end_time = feature_start_time + pd.Timedelta(self.sample_freq) * (self.samples_in_node_feature)
        target_start_time = feature_end_time
        target_end_time = target_start_time + pd.Timedelta(self.sample_freq) * (self.samples_in_node_target)

        if self.verbose:
            print(f"feature_start_time: {feature_start_time}")
            print(f"feature_end_time: {feature_end_time}")
            print(f"target_start_time: {target_start_time}")
            print(f"target_end_time: {target_end_time}")
            print(f"time index start: {time_index_start}")
            print(f"time index end: {time_index_end}")
            print(f"current graph index start: {current_graph_index_start}")
            print(f"current graph index end: {current_graph_index_end}")

        start_idx, end_idx = time_index_start-current_graph_index_start, time_index_end-current_graph_index_start
        node_features = self.current_graph_data.x[:, start_idx:start_idx+self.samples_in_node_feature]
        node_targets = self.current_graph_data.y[:, start_idx+self.samples_in_node_feature:end_idx]
        node_features_mask = self.current_graph_data.node_features_mask[:, start_idx:start_idx+self.samples_in_node_feature]
        node_targets_mask = self.current_graph_data.node_targets_mask[:, start_idx+self.samples_in_node_feature:end_idx]
        # determine if we have all data in memory
        if time_index_end >= current_graph_index_end:
            # load the next graph(s)
            self._load_next_graph()

        if self.verbose:
            # print shapes
            print(f"node_features shape: {node_features.shape}")
            print(f"node_targets shape: {node_targets.shape}")
            print(f"node_features_mask shape: {node_features_mask.shape}")
            print(f"node_targets_mask shape: {node_targets_mask.shape}")
            print(f"edge_index shape: {edge_index.shape}")
            print(f"edge_attr shape: {edge_attr.shape}")

        # we need to compute the rest of the masks
        valid_measurement_mask = torch.cat((node_features_mask, node_targets_mask), dim=1)
        node_all_valid_measurements_mask = torch.all(valid_measurement_mask, dim=1)
        edge_node_all_valid_measurements_mask = torch.logical_and(node_all_valid_measurements_mask[edge_index[0]], node_all_valid_measurements_mask[edge_index[1]])

        data = Data(
            x=node_features,
            y=node_targets,
            edge_index=edge_index,
            edge_attr=edge_attr,
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
