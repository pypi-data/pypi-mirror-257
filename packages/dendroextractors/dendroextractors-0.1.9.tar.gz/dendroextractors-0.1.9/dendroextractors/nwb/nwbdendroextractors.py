from __future__ import annotations
from pathlib import Path
from typing import List, Optional, Literal, Dict, BinaryIO
import warnings

import numpy as np

from spikeinterface import get_global_tmp_folder
from spikeinterface.core import BaseRecording, BaseRecordingSegment
from spikeinterface.core.core_tools import define_function_from_class

import time


def import_lazily():
    "Makes annotations / typing available lazily"
    global NWBFile, ElectricalSeries, Units, NWBHDF5IO
    from pynwb import NWBFile
    from pynwb.ecephys import ElectricalSeries
    from pynwb.misc import Units
    from pynwb import NWBHDF5IO


def read_file_from_backend(
    *,
    file_path: str | Path | None,
    file: BinaryIO | None = None,
    stream_mode: Literal["ffspec", "ros3", "remfile", "dendro"] | None = None,
    cache: bool = False,
    stream_cache_path: str | Path | None = None,
    storage_options: dict | None = None,
    backend: Literal["hdf5", "zarr"] | None = None,
):
    """
    Reads a file from a hdf5 or zarr backend.
    """
    if stream_mode == "fsspec":
        import h5py
        import fsspec
        from fsspec.implementations.cached import CachingFileSystem

        assert file_path is not None, "file_path must be specified when using stream_mode='fsspec'"

        fsspec_file_system = fsspec.filesystem("http")

        if cache:
            stream_cache_path = stream_cache_path if stream_cache_path is not None else str(get_global_tmp_folder())
            caching_file_system = CachingFileSystem(
                fs=fsspec_file_system,
                cache_storage=str(stream_cache_path),
            )
            ffspec_file = caching_file_system.open(path=file_path, mode="rb")
        else:
            ffspec_file = fsspec_file_system.open(file_path, "rb")

        if _is_hdf5_file(ffspec_file):
            open_file = h5py.File(ffspec_file, "r")
        else:
            raise RuntimeError(f"{file_path} is not a valid HDF5 file!")

    elif stream_mode == "ros3":
        import h5py

        assert file_path is not None, "file_path must be specified when using stream_mode='ros3'"

        drivers = h5py.registered_drivers()
        assertion_msg = "ROS3 support not enbabled, use: install -c conda-forge h5py>=3.2 to enable streaming"
        assert "ros3" in drivers, assertion_msg
        open_file = h5py.File(name=file_path, mode="r", driver="ros3")

    elif stream_mode == "remfile":
        import remfile
        import h5py

        assert file_path is not None, "file_path must be specified when using stream_mode='remfile'"
        rfile = remfile.File(file_path)
        if _is_hdf5_file(rfile):
            open_file = h5py.File(rfile, "r")
        else:
            raise RuntimeError(f"{file_path} is not a valid HDF5 file!")

    elif stream_mode == "dendro":
        from dendro.sdk import get_project_file_from_uri
        import h5py

        assert file_path is not None, "file_path must be specified when using stream_mode='dendro'"
        if not str(file_path).startswith('dendro:?'):
            raise Exception(f"Invalid dendro project file URI: {file_path}")
        input_file = get_project_file_from_uri(str(file_path))
        ff = input_file.get_file()
        open_file = h5py.File(ff, "r")

    elif stream_mode == "zarr":
        import zarr

        open_file = zarr.open(file_path, mode="r", storage_options=storage_options)

    elif file_path is not None:  # local
        file_path = str(Path(file_path).resolve())
        backend = _get_backend_from_local_file(file_path)
        if backend == "zarr":
            import zarr

            open_file = zarr.open(file_path, mode="r")
        else:
            import h5py

            open_file = h5py.File(name=file_path, mode="r")
    else:
        import h5py

        assert file is not None, "Unexpected, file is None"
        open_file = h5py.File(file, "r")

    return open_file


def read_nwbfile(
    *,
    backend: Literal["hdf5", "zarr"],
    file_path: str | Path | None,
    file: BinaryIO | None = None,
    stream_mode: Literal["ffspec", "ros3", "remfile", "dendro", "zarr"] | None = None,
    cache: bool = False,
    stream_cache_path: str | Path | None = None,
    storage_options: dict | None = None,
) -> NWBFile:
    """
    Read an NWB file and return the NWBFile object.

    Parameters
    ----------
    file_path : Path, str or None
        The path to the NWB file. Either provide this or file.
    file : file-like object or None
        The file-like object to read from. Either provide this or file_path.
    stream_mode : "fsspec" | "ros3" | "remfile" | "dendro" | None, default: None
        The streaming mode to use. If None it assumes the file is on the local disk.
    cache: bool, default: False
        If True, the file is cached in the file passed to stream_cache_path
        if False, the file is not cached.
    stream_cache_path : str or None, default: None
        The path to the cache storage, when default to None it uses the a temporary
        folder.
    Returns
    -------
    nwbfile : NWBFile
        The NWBFile object.

    Raises
    ------
    AssertionError
        If ROS3 support is not enabled.

    Notes
    -----
    This function can stream data from the "fsspec", "ros3" and "rem" protocols.


    Examples
    --------
    >>> nwbfile = read_nwbfile(file_path="data.nwb", backend="hdf5", stream_mode="ros3")
    """

    if file_path is not None and file is not None:
        raise ValueError("Provide either file_path or file, not both")
    if file_path is None and file is None:
        raise ValueError("Provide either file_path or file")

    open_file = read_file_from_backend(
        file_path=file_path,
        file=file,
        stream_mode=stream_mode,
        cache=cache,
        stream_cache_path=stream_cache_path,
        storage_options=storage_options,
    )
    if backend == "hdf5":
        from pynwb import NWBHDF5IO

        io = NWBHDF5IO(file=open_file, mode="r", load_namespaces=True)
    else:
        from hdmf_zarr import NWBZarrIO

        io = NWBZarrIO(path=open_file.store, mode="r", load_namespaces=True)

    nwbfile = io.read()
    return nwbfile


def _retrieve_electrical_series_pynwb(
    nwbfile: NWBFile, electrical_series_path: Optional[str] = None
) -> ElectricalSeries:
    """
    Get an ElectricalSeries object from an NWBFile.

    Parameters
    ----------
    nwbfile : NWBFile
        The NWBFile object from which to extract the ElectricalSeries.
    electrical_series_path : str, default: None
        The name of the ElectricalSeries to extract. If not specified, it will return the first found ElectricalSeries
        if there's only one; otherwise, it raises an error.

    Returns
    -------
    ElectricalSeries
        The requested ElectricalSeries object.

    Raises
    ------
    ValueError
        If no acquisitions are found in the NWBFile or if multiple acquisitions are found but no electrical_series_path
        is provided.
    AssertionError
        If the specified electrical_series_path is not present in the NWBFile.
    """
    from pynwb.ecephys import ElectricalSeries

    electrical_series_dict: Dict[str, ElectricalSeries] = {}

    for item in nwbfile.all_children():
        if isinstance(item, ElectricalSeries):
            # remove data and skip first "/"
            electrical_series_key = item.data.name.replace("/data", "")[1:]
            electrical_series_dict[electrical_series_key] = item

    if electrical_series_path is not None:
        if electrical_series_path not in electrical_series_dict:
            raise ValueError(f"{electrical_series_path} not found in the NWBFile. ")
        electrical_series = electrical_series_dict[electrical_series_path]
    else:
        electrical_series_list = list(electrical_series_dict.keys())
        if len(electrical_series_list) > 1:
            raise ValueError(
                f"More than one acquisition found! You must specify 'electrical_series_path'. \n"
                f"Options in current file are: {[e for e in electrical_series_list]}"
            )
        if len(electrical_series_list) == 0:
            raise ValueError("No acquisitions found in the .nwb file.")
        electrical_series = electrical_series_dict[electrical_series_list[0]]

    return electrical_series


def _retrieve_unit_table_pynwb(nwbfile: NWBFile, unit_table_path: Optional[str] = None) -> Units:
    """
    Get an Units object from an NWBFile.
    Units tables can be either the main unit table (nwbfile.units) or in the processing module.

    Parameters
    ----------
    nwbfile : NWBFile
        The NWBFile object from which to extract the Units.
    unit_table_path : str, default: None
        The path of the Units to extract. If not specified, it will return the first found Units
        if there's only one; otherwise, it raises an error.

    Returns
    -------
    Units
        The requested Units object.

    Raises
    ------
    ValueError
        If no unit tables are found in the NWBFile or if multiple unit tables are found but no unit_table_path
        is provided.
    AssertionError
        If the specified unit_table_path is not present in the NWBFile.
    """
    from pynwb.misc import Units

    unit_table_dict: Dict[str:Units] = {}

    for item in nwbfile.all_children():
        if isinstance(item, Units):
            # retrieve name of "id" column and skip first "/"
            unit_table_key = item.id.data.name.replace("/id", "")[1:]
            unit_table_dict[unit_table_key] = item

    if unit_table_path is not None:
        if unit_table_path not in unit_table_dict:
            raise ValueError(f"{unit_table_path} not found in the NWBFile. ")
        unit_table = unit_table_dict[unit_table_path]
    else:
        unit_table_list: List[Units] = list(unit_table_dict.keys())

        if len(unit_table_list) > 1:
            raise ValueError(
                f"More than one unit table found! You must specify 'unit_table_list_name'. \n"
                f"Options in current file are: {[e for e in unit_table_list]}"
            )
        if len(unit_table_list) == 0:
            raise ValueError("No unit table found in the .nwb file.")
        unit_table = unit_table_dict[unit_table_list[0]]

    return unit_table


def _is_hdf5_file(filename_or_file):
    # Source for magic numbers https://www.loc.gov/preservation/digital/formats/fdd/fdd000229.shtml
    # We should find a better one though
    if isinstance(filename_or_file, (str, Path)):
        with open(filename_or_file, "rb") as f:
            file_signature = f.read(8)
    else:
        file_signature = filename_or_file.read(8)
    return file_signature == b"\x89HDF\r\n\x1a\n"


def _get_backend_from_local_file(file_path: str | Path) -> str:
    """
    Returns the file backend from a file path ("hdf5", "zarr")

    Parameters
    ----------
    file_path : str or Path
        The path to the file.

    Returns
    -------
    backend : str
        The file backend ("hdf5", "zarr")
    """
    file_path = Path(file_path)
    if file_path.is_file():
        if _is_hdf5_file(file_path):
            backend = "hdf5"
        else:
            raise RuntimeError(f"{file_path} is not a valid HDF5 file!")
    elif file_path.is_dir():
        try:
            import zarr

            with zarr.open(file_path, "r") as f:
                backend = "zarr"
        except:
            raise RuntimeError(f"{file_path} is not a valid Zarr folder!")
    else:
        raise RuntimeError(f"File {file_path} is not an existing file or folder!")
    return backend


def _find_neurodata_type_from_backend(group, path="", result=None, neurodata_type="ElectricalSeries", backend="hdf5"):
    """
    Recursively searches for groups with the specified neurodata_type hdf5 or zarr object,
    and returns a list with their paths.
    """
    if backend == "hdf5":
        import h5py

        group_class = h5py.Group
    else:
        import zarr

        group_class = zarr.Group

    if result is None:
        result = []

    for neurodata_name, value in group.items():
        # Check if it's a group and if it has the neurodata_type
        if isinstance(value, group_class):
            current_path = f"{path}/{neurodata_name}" if path else neurodata_name
            if value.attrs.get("neurodata_type") == neurodata_type:
                result.append(current_path)
            _find_neurodata_type_from_backend(
                value, current_path, result, neurodata_type, backend
            )  # Recursive call for sub-groups
    return result


def _fetch_time_info_pynwb(electrical_series, samples_for_rate_estimation, load_time_vector=False):
    """
    Extracts the sampling frequency and the time vector from an ElectricalSeries object.
    """
    sampling_frequency = None
    if hasattr(electrical_series, "rate"):
        sampling_frequency = electrical_series.rate

    if hasattr(electrical_series, "starting_time"):
        t_start = electrical_series.starting_time
    else:
        t_start = None

    timestamps = None
    if hasattr(electrical_series, "timestamps"):
        if electrical_series.timestamps is not None:
            timestamps = electrical_series.timestamps
            t_start = electrical_series.timestamps[0]

    # TimeSeries need to have either timestamps or rate
    if sampling_frequency is None:
        sampling_frequency = 1.0 / np.median(np.diff(timestamps[:samples_for_rate_estimation]))

    if load_time_vector and timestamps is not None:
        times_kwargs = dict(time_vector=electrical_series.timestamps)
    else:
        times_kwargs = dict(sampling_frequency=sampling_frequency, t_start=t_start)

    return sampling_frequency, times_kwargs


def _retrieve_electrodes_indices_from_electrical_series_backend(open_file, electrical_series, backend="hdf5"):
    """
    Retrieves the indices of the electrodes from the electrical series.
    For the Zarr backend, the electrodes are stored in the electrical_series.attrs["zarr_link"].
    """
    if "electrodes" not in electrical_series:
        if backend == "zarr":
            import zarr

            # links must be resolved
            zarr_links = electrical_series.attrs["zarr_link"]
            electrodes_path = None
            for zarr_link in zarr_links:
                if zarr_link["name"] == "electrodes":
                    electrodes_path = zarr_link["path"]
            assert electrodes_path is not None, "electrodes must be present in the electrical series"
            electrodes_indices = open_file[electrodes_path][:]
        else:
            raise ValueError("electrodes must be present in the electrical series")
    else:
        electrodes_indices = electrical_series["electrodes"][:]
    return electrodes_indices


class NwbDendroRecordingExtractor(BaseRecording):
    """Load an NWBFile as a RecordingExtractor.

    Parameters
    ----------
    file_path: str, Path, or None
        Path to the NWB file or an s3 URL. Use this parameter to specify the file location
        if not using the `file` parameter.
    electrical_series_name: str or None, default: None
        Deprecated, use `electrical_series_path` instead.
    electrical_series_path: str or None, default: None
        The name of the ElectricalSeries object within the NWB file. This parameter is crucial
        when the NWB file contains multiple ElectricalSeries objects. It helps in identifying
        which specific series to extract data from. If there is only one ElectricalSeries and
        this parameter is not set, that unique series will be used by default.
        If multiple ElectricalSeries are present and this parameter is not set, an error is raised.
        The `electrical_series_path` corresponds to the path within the NWB file, e.g.,
        'acquisition/MyElectricalSeries`.
    load_time_vector: bool, default: False
        If set to True, the time vector is also loaded into the recording object. Useful for
        cases where precise timing information is required.
    samples_for_rate_estimation: int, default: 1000
        The number of timestamp samples used for estimating the sampling rate. This is relevant
        when the 'rate' attribute is not available in the ElectricalSeries.
    stream_mode : "fsspec" | "ros3" | "remfile" | "dendro" | "zarr" | None, default: None
        Determines the streaming mode for reading the file. Use this for optimized reading from
        different sources, such as local disk or remote servers.
    load_channel_properties: bool, default: True
        If True, all the channel properties are loaded from the NWB file and stored as properties.
        For streaming purposes, it can be useful to set this to False to speed up streaming.
    file: file-like object or None, default: None
        A file-like object representing the NWB file. Use this parameter if you have an in-memory
        representation of the NWB file instead of a file path.
    cache: bool, default: False
        Indicates whether to cache the file locally when using streaming. Caching can improve performance for
        remote files.
    stream_cache_path: str, Path, or None, default: None
        Specifies the local path for caching the file. Relevant only if `cache` is True.
    storage_options: dict | None = None,
        Additional parameters for the storage backend (e.g. AWS credentials) used for "zarr" stream_mode.
    use_pynwb: bool, default: False
        Uses the pynwb library to read the NWB file. Setting this to False, the default, uses h5py
        to read the file. Using h5py can improve performance by bypassing some of the PyNWB validations.

    Returns
    -------
    recording : NwbDendroRecordingExtractor
        The recording extractor for the NWB file.

    Examples
    --------
    Run on local file:

    >>> from dendroextractors.nwb.nwbdendroextractors import NwbDendroRecordingExtractor
    >>> rec = NwbDendroRecordingExtractor(filepath)

    Run on s3 URL from the DANDI Archive:

    >>> from spikeinterface.extractors.nwbextractors import NwbDendroRecordingExtractor
    >>> from dandi.dandiapi import DandiAPIClient
    >>>
    >>> # get s3 path
    >>> dandiset_id, filepath = "101116", "sub-001/sub-001_ecephys.nwb"
    >>> with DandiAPIClient("https://api-staging.dandiarchive.org/api") as client:
    >>>     asset = client.get_dandiset(dandiset_id, "draft").get_asset_by_path(filepath)
    >>>     s3_url = asset.get_content_url(follow_redirects=1, strip_query=True)
    >>>
    >>> rec = NwbDendroRecordingExtractor(s3_url, stream_mode="fsspec", stream_cache_path="cache")
    """

    extractor_name = "NwbDendroRecording"
    mode = "file"
    name = "nwb"
    installation_mesg = "To use the Nwb extractors, install pynwb: \n\n pip install pynwb\n\n"

    def __init__(
        self,
        file_path: str | Path | None = None,  # provide either this or file
        electrical_series_name: str | None = None,  # deprecated
        load_time_vector: bool = False,
        samples_for_rate_estimation: int = 1_000,
        stream_mode: Optional[Literal["fsspec", "ros3", "remfile", "dendro", "zarr"]] = None,
        stream_cache_path: str | Path | None = None,
        electrical_series_path: str | None = None,
        load_channel_properties: bool = True,
        *,
        file: BinaryIO | None = None,  # file-like - provide either this or file_path
        cache: bool = False,
        storage_options: dict | None = None,
        use_pynwb: bool = False,
    ):
        if file_path is not None and file is not None:
            raise ValueError("Provide either file_path or file, not both")
        if file_path is None and file is None:
            raise ValueError("Provide either file_path or file")

        if electrical_series_name is not None:
            warning_msg = (
                "The `electrical_series_name` parameter is deprecated and will be removed in version 0.101.0.\n"
                "Use `electrical_series_path` instead."
            )
            if electrical_series_path is None:
                warning_msg += f"\nSetting `electrical_series_path` to 'acquisition/{electrical_series_name}'."
                electrical_series_path = f"acquisition/{electrical_series_name}"
            else:
                warning_msg += f"\nIgnoring `electrical_series_name` and using the provided `electrical_series_path`."
            warnings.warn(warning_msg, DeprecationWarning, stacklevel=2)

        self.file_path = file_path
        self.stream_mode = stream_mode
        self.stream_cache_path = stream_cache_path
        self.storage_options = storage_options
        self.electrical_series_path = electrical_series_path

        if self.stream_mode is None and file is None:
            self.backend = _get_backend_from_local_file(file_path)
        else:
            if self.stream_mode == "zarr":
                self.backend = "zarr"
            else:
                self.backend = "hdf5"

        # extract info
        if use_pynwb:
            try:
                import pynwb
            except ImportError:
                raise ImportError(self.installation_mesg)

            (
                channel_ids,
                sampling_frequency,
                dtype,
                segment_data,
                times_kwargs,
            ) = self._fetch_recording_segment_info_pynwb(file, cache, load_time_vector, samples_for_rate_estimation)
        else:
            (
                channel_ids,
                sampling_frequency,
                dtype,
                segment_data,
                times_kwargs,
            ) = self._fetch_recording_segment_info_backend(file, cache, load_time_vector, samples_for_rate_estimation)

        BaseRecording.__init__(self, channel_ids=channel_ids, sampling_frequency=sampling_frequency, dtype=dtype)
        recording_segment = NwbDendroRecordingSegment(
            electrical_series_data=segment_data,
            times_kwargs=times_kwargs,
        )
        self.add_recording_segment(recording_segment)

        # fetch and add main recording properties
        if use_pynwb:
            gains, offsets, locations, groups = self._fetch_main_properties_pynwb()
        else:
            gains, offsets, locations, groups = self._fetch_main_properties_backend()
        self.set_channel_gains(gains)
        self.set_channel_offsets(offsets)
        if locations is not None:
            self.set_channel_locations(locations)
        if groups is not None:
            self.set_channel_groups(groups)

        # fetch and add additional recording properties
        if load_channel_properties:
            if use_pynwb:
                electrodes_table = self._nwbfile.electrodes
                electrodes_indices = self.electrical_series.electrodes.data[:]
                columns = electrodes_table.colnames
            else:
                electrodes_table = self._file["/general/extracellular_ephys/electrodes"]
                electrodes_indices = _retrieve_electrodes_indices_from_electrical_series_backend(
                    self._file, self.electrical_series, self.backend
                )
                columns = electrodes_table.attrs["colnames"]
            properties = self._fetch_other_properties(electrodes_table, electrodes_indices, columns)

            for property_name, property_values in properties.items():
                values = [x.decode("utf-8") if isinstance(x, bytes) else x for x in property_values]
                self.set_property(property_name, values)

        if stream_mode is None and file_path is not None:
            file_path = str(Path(file_path).resolve())

        if stream_mode == "fsspec" and stream_cache_path is not None:
            stream_cache_path = str(Path(self.stream_cache_path).absolute())

        # set serializability bools
        if file is not None:
            # not json serializable if file arg is provided
            self._serializability["json"] = False

        if storage_options is not None and stream_mode == "zarr":
            warnings.warn(
                "The `storage_options` parameter will not be propagated to JSON or pickle files for security reasons, "
                "so the extractor will not be JSON/pickle serializable. Only in-memory mode will be available."
            )
            # not serializable if storage_options is provided
            self._serializability["json"] = False
            self._serializability["pickle"] = False

        self._kwargs = {
            "file_path": file_path,
            "electrical_series_path": self.electrical_series_path,
            "load_time_vector": load_time_vector,
            "samples_for_rate_estimation": samples_for_rate_estimation,
            "stream_mode": stream_mode,
            "load_channel_properties": load_channel_properties,
            "storage_options": storage_options,
            "cache": cache,
            "stream_cache_path": stream_cache_path,
            "file": file,
        }

    def __del__(self):
        # backend mode
        if hasattr(self, "_file"):
            if hasattr(self._file, "store"):
                self._file.store.close()
            else:
                self._file.close()
        # pynwb mode
        elif hasattr(self, "_nwbfile"):
            io = self._nwbfile.get_read_io()
            if io is not None:
                io.close()

    def _fetch_recording_segment_info_pynwb(self, file, cache, load_time_vector, samples_for_rate_estimation):
        self._nwbfile = read_nwbfile(
            backend=self.backend,
            file_path=self.file_path,
            file=file,
            stream_mode=self.stream_mode,
            cache=cache,
            stream_cache_path=self.stream_cache_path,
        )
        electrical_series = _retrieve_electrical_series_pynwb(self._nwbfile, self.electrical_series_path)
        # The indices in the electrode table corresponding to this electrical series
        electrodes_indices = electrical_series.electrodes.data[:]
        # The table for all the electrodes in the nwbfile
        electrodes_table = self._nwbfile.electrodes

        sampling_frequency, times_kwargs = _fetch_time_info_pynwb(
            electrical_series=electrical_series,
            samples_for_rate_estimation=samples_for_rate_estimation,
            load_time_vector=load_time_vector,
        )

        # Fill channel properties dictionary from electrodes table
        if "channel_name" in electrodes_table.colnames:
            channel_ids = [
                electrical_series.electrodes["channel_name"][electrodes_index]
                for electrodes_index in electrodes_indices
            ]
        else:
            channel_ids = [electrical_series.electrodes.table.id[x] for x in electrodes_indices]
        electrical_series_data = electrical_series.data
        dtype = electrical_series_data.dtype

        # need this later
        self.electrical_series = electrical_series

        return channel_ids, sampling_frequency, dtype, electrical_series_data, times_kwargs

    def _fetch_recording_segment_info_backend(self, file, cache, load_time_vector, samples_for_rate_estimation):
        open_file = read_file_from_backend(
            backend=self.backend,
            file_path=self.file_path,
            file=file,
            stream_mode=self.stream_mode,
            cache=cache,
            stream_cache_path=self.stream_cache_path,
        )

        # If the electrical_series_path is not given, `_find_neurodata_type_from_backend` will be called
        # And returns a list with the electrical_series_paths available in the file.
        # If there is only one electrical series, the electrical_series_path is set to the name of the series,
        # otherwise an error is raised.
        if self.electrical_series_path is None:
            available_electrical_series = _find_neurodata_type_from_backend(
                open_file, neurodata_type="ElectricalSeries", backend=self.backend
            )
            # if electrical_series_path is None:
            if len(available_electrical_series) == 1:
                self.electrical_series_path = available_electrical_series[0]
            else:
                raise ValueError(
                    "Multiple ElectricalSeries found in the file. "
                    "Please specify the 'electrical_series_path' argument:"
                    f"Available options are: {available_electrical_series}."
                )

        # Open the electrical series. In case of failure, raise an error with the available options.
        try:
            electrical_series = open_file[self.electrical_series_path]
        except KeyError:
            available_electrical_series = _find_neurodata_type_from_backend(
                open_file, neurodata_type="ElectricalSeries", backend=self.backend
            )
            raise ValueError(
                f"{self.electrical_series_path} not found in the NWB file!"
                f"Available options are: {available_electrical_series}."
            )
        electrodes_indices = _retrieve_electrodes_indices_from_electrical_series_backend(
            open_file, electrical_series, self.backend
        )
        # The table for all the electrodes in the nwbfile
        electrodes_table = open_file["/general/extracellular_ephys/electrodes"]
        electrode_table_columns = electrodes_table.attrs["colnames"]

        # Get sampling frequency
        if "starting_time" in electrical_series.keys():
            t_start = electrical_series["starting_time"][()]
            sampling_frequency = electrical_series["starting_time"].attrs["rate"]
        elif "timestamps" in electrical_series.keys():
            timestamps = electrical_series["timestamps"][:]
            t_start = timestamps[0]
            sampling_frequency = 1.0 / np.median(np.diff(timestamps[:samples_for_rate_estimation]))

        if load_time_vector and timestamps is not None:
            times_kwargs = dict(time_vector=electrical_series.timestamps)
        else:
            times_kwargs = dict(sampling_frequency=sampling_frequency, t_start=t_start)

        # If channel names are present, use them as channel_ids instead of the electrode ids
        if "channel_name" in electrode_table_columns:
            channel_names = electrodes_table["channel_name"]
            channel_ids = channel_names[electrodes_indices]
            # Decode if bytes with utf-8
            channel_ids = [x.decode("utf-8") if isinstance(x, bytes) else x for x in channel_ids]

        else:
            channel_ids = [electrodes_table["id"][x] for x in electrodes_indices]

        dtype = electrical_series["data"].dtype
        electrical_series_data = electrical_series["data"]

        # need this for later
        self.electrical_series = electrical_series
        self._file = open_file

        return channel_ids, sampling_frequency, dtype, electrical_series_data, times_kwargs

    def _fetch_locations_and_groups(self, electrodes_table, electrodes_indices):
        # Channel locations
        locations = None
        if "rel_x" in electrodes_table:
            if "rel_y" in electrodes_table:
                ndim = 3 if "rel_z" in electrodes_table else 2
                locations = np.zeros((self.get_num_channels(), ndim), dtype=float)
                locations[:, 0] = electrodes_table["rel_x"][electrodes_indices]
                locations[:, 1] = electrodes_table["rel_y"][electrodes_indices]
                if "rel_z" in electrodes_table:
                    locations[:, 2] = electrodes_table["rel_z"][electrodes_indices]

        # Channel groups
        groups = None
        if "group_name" in electrodes_table:
            groups = electrodes_table["group_name"][electrodes_indices][:]
        if groups is not None:
            groups = np.array([x.decode("utf-8") if isinstance(x, bytes) else x for x in groups])
        return locations, groups

    def _fetch_other_properties(self, electrodes_table, electrodes_indices, columns):
        #########
        # Extract and re-name properties from nwbfile TODO: Should be a function
        ########
        from pynwb.ecephys import ElectrodeGroup

        properties = dict()
        properties_to_skip = [
            "id",
            "rel_x",
            "rel_y",
            "rel_z",
            "group",
            "group_name",
            "channel_name",
            "offset",
        ]
        rename_properties = dict(location="brain_area")

        for column in columns:
            first_value = electrodes_table[column][0]
            if isinstance(first_value, ElectrodeGroup):
                continue
            elif column in properties_to_skip:
                continue
            else:
                column_name = rename_properties.get(column, column)
                properties[column_name] = electrodes_table[column][electrodes_indices]

        return properties

    def _fetch_main_properties_pynwb(self):
        """
        Fetches the main properties from the NWBFile and stores them in the RecordingExtractor, including:

        - gains
        - offsets
        - locations
        - groups
        """
        electrodes_indices = self.electrical_series.electrodes.data[:]
        electrodes_table = self._nwbfile.electrodes

        # Channels gains - for RecordingExtractor, these are values to cast traces to uV
        gains = self.electrical_series.conversion * 1e6
        if self.electrical_series.channel_conversion is not None:
            gains = self.electrical_series.conversion * self.electrical_series.channel_conversion[:] * 1e6

        # Channel offsets
        offset = self.electrical_series.offset if hasattr(self.electrical_series, "offset") else 0
        if offset == 0 and "offset" in electrodes_table:
            offset = electrodes_table["offset"].data[electrodes_indices]
        offsets = offset * 1e6

        locations, groups = self._fetch_locations_and_groups(electrodes_table, electrodes_indices)

        return gains, offsets, locations, groups

    def _fetch_main_properties_backend(self):
        """
        Fetches the main properties from the NWBFile and stores them in the RecordingExtractor, including:

        - gains
        - offsets
        - locations
        - groups
        """
        electrodes_indices = _retrieve_electrodes_indices_from_electrical_series_backend(
            self._file, self.electrical_series, self.backend
        )
        electrodes_table = self._file["/general/extracellular_ephys/electrodes"]

        # Channels gains - for RecordingExtractor, these are values to cast traces to uV
        data_attributes = self.electrical_series["data"].attrs
        electrical_series_conversion = data_attributes["conversion"]
        gains = electrical_series_conversion * 1e6
        if "channel_conversion" in data_attributes:
            gains *= self.electrical_series["channel_conversion"][:]

        # Channel offsets
        offset = data_attributes["offset"] if "offset" in data_attributes else 0
        if offset == 0 and "offset" in electrodes_table:
            offset = electrodes_table["offset"][electrodes_indices]
        offsets = offset * 1e6

        # Channel locations and groups
        locations, groups = self._fetch_locations_and_groups(electrodes_table, electrodes_indices)

        return gains, offsets, locations, groups


class NwbDendroRecordingSegment(BaseRecordingSegment):
    def __init__(self, electrical_series_data, times_kwargs):
        BaseRecordingSegment.__init__(self, **times_kwargs)
        self.electrical_series_data = electrical_series_data
        self._num_samples = self.electrical_series_data.shape[0]

    def get_num_samples(self):
        """Returns the number of samples in this signal block

        Returns:
            SampleIndex: Number of samples in the signal block
        """
        return self._num_samples

    def get_traces(
        self,
        start_frame: int | None = None,
        end_frame: int | None = None,
        channel_indices=None
    ):
        try:
            traces = self.get_traces_try(start_frame, end_frame, channel_indices)
            return traces
        except Exception as e:
            print(f"Error when trying to get traces: {e}")
            print(f'start_frame = {start_frame}, end_frame = {end_frame}, channel_indices = {channel_indices}')
            print(f'num_samples = {self.get_num_samples()}')
            print(f'electrical_series_data.shape = {self.electrical_series_data.shape}')
            raise e

    def get_traces_try(self, start_frame, end_frame, channel_indices):
        if start_frame is None:
            start_frame = 0
        if end_frame is None:
            end_frame = self.get_num_samples()

        electrical_series_data = self.electrical_series_data
        if electrical_series_data.ndim == 1:
            traces = electrical_series_data[start_frame:end_frame][:, np.newaxis]
        elif isinstance(channel_indices, slice):
            traces = electrical_series_data[start_frame:end_frame, channel_indices]
        else:
            # channel_indices is np.ndarray
            if np.array(channel_indices).size > 1 and np.any(np.diff(channel_indices) < 0):
                # get around h5py constraint that it does not allow datasets
                # to be indexed out of order
                sorted_channel_indices = np.sort(channel_indices)
                resorted_indices = np.array([list(sorted_channel_indices).index(ch) for ch in channel_indices])
                recordings = electrical_series_data[start_frame:end_frame, sorted_channel_indices]
                traces = recordings[:, resorted_indices]
            else:
                traces = electrical_series_data[start_frame:end_frame, channel_indices]

        return traces


def _jitter(max_jitter):
    from random import random
    return max_jitter * (random() * 2 - 1)


read_nwb_recording = define_function_from_class(source_class=NwbDendroRecordingExtractor, name="read_nwb_recording")
