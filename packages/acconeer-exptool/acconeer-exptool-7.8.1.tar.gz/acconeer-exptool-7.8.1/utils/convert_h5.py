# Copyright (c) Acconeer AB, 2022-2024
# All rights reserved


from __future__ import annotations

import abc
import argparse
import json
import os
import typing as t
from pathlib import Path
from typing import Optional, Tuple, Union

import h5py
import numpy as np
import numpy.typing as npt
import pandas as pd

import acconeer.exptool as et
import acconeer.exptool.a121.algo.breathing as breathing
import acconeer.exptool.a121.algo.presence as presence
import acconeer.exptool.a121.algo.surface_velocity as surface_velocity
from acconeer.exptool import a121
from acconeer.exptool.a121 import H5Record, _core, algo
from acconeer.exptool.a121._core_ext._replaying_client import _ReplayingClient


try:
    import prettyprinter  # type: ignore[import-not-found]

    prettyprinter.install_extras(["attrs"])

    pprint = prettyprinter.cpprint
except ImportError:
    from pprint import pprint


DESCRIPTION = """This is a command line utility that lets you convert
.h5/.npz files to .csv-files for use as is or in
e.g. Microsoft Excel.

example usage:
  python3 convert_h5.py -v ~/my_data_file.h5 ~/my_output_file.csv
"""


class ConvertToCsvArgumentParser(argparse.ArgumentParser):
    def __init__(self) -> None:
        super().__init__(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
        self.add_argument(
            "input_file",
            type=Path,
            help='The input file with file endings ".h5" or ".npz" (only A111).',
        )
        self.add_argument(
            "output_file",
            type=Path,
            nargs="?",
            default=None,
            help="The output file to which h5-data will be written.",
        )
        self.add_argument(
            "--index",
            "--id",
            "--sensor",
            metavar="index/id",
            dest="sensor",
            type=int,
            default=argparse.SUPPRESS,
            help="The sensor index. Gets data from a specific sensor when multiple sensors are "
            "used.",
        )
        self.add_argument(
            "-f",
            "--force",
            action="store_true",
            default=False,
            help='Forcefully overwrite "output_file" if it already exists.',
        )
        self.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            default=False,
            help='Prints meta data from "input_file".',
        )
        self.add_argument(
            "--sweep-as-column",
            action="store_true",
            default=False,
            help="Stores sweeps as columns instead of rows.\n"
            "The default is to store sweeps as rows.",
        )
        self.add_argument(
            "-m",
            "--add_sweep_metadata",
            action="store_true",
            default=False,
            help="Adds depth and sweep number info to the csv file",
        )


class TableConverter:
    @abc.abstractmethod
    def convert(self, sensor: int) -> npt.NDArray[t.Any]:
        pass

    @abc.abstractmethod
    def get_metadata_rows(self, sensor: int) -> list[npt.NDArray[t.Any]]:
        pass

    @abc.abstractmethod
    def print_information(self, verbose: bool = False) -> None:
        pass

    @staticmethod
    def format_cell_value(v: t.Any) -> str:
        if isinstance(v, complex):
            return f"{np.real(v):0}{np.imag(v):+}j"
        else:
            return str(v)

    @classmethod
    def from_record(cls, record: Union[et.a111.recording.Record, a121.Record]) -> TableConverter:
        if isinstance(record, et.a111.recording.Record):
            return A111RecordTableConverter(record)
        elif isinstance(record, a121.Record):
            return A121RecordTableConverter(record)
        else:
            raise ValueError(f"Passed record ({record}) was of unexpected type.")


class A111RecordTableConverter(TableConverter):
    def __init__(self, record: et.a111.recording.Record) -> None:
        self._record = record

    def get_metadata_rows(self, sensor: int) -> list[npt.NDArray[t.Any]]:
        depths = et.a111.get_range_depths(self._record.sensor_config, self._record.session_info)
        num_points = len(depths)
        rounded_depths = np.round(depths, decimals=6)

        if self._record.mode != et.a111.Mode.SPARSE:
            return [rounded_depths]
        else:
            spf = self._record.sensor_config.sweeps_per_frame
            sweep_numbers = np.repeat(range(spf), repeats=num_points).astype(int)
            depths_header = np.tile(rounded_depths, spf)
            return [sweep_numbers, depths_header]

    def convert(self, sensor: int) -> npt.NDArray[t.Any]:
        """Converts data of a single sensor

        :param sensor: The sensor index
        :returns: 2D NDArray of cell values.
        """
        record = self._record
        sensor_index = sensor

        num_sensors = record.data.shape[1]
        if sensor_index >= num_sensors:
            raise ValueError(
                f"Invalid sensor index specified (index={sensor_index}). "
                f"Valid indices for this input file is one of {list(range(num_sensors))}"
            )

        data = record.data[:, sensor_index, :]
        dest_rows = []

        for x in data:
            row = np.ndarray.flatten(x)
            dest_rows.append([self.format_cell_value(v) for v in row])

        return np.array(dest_rows)

    def print_information(self, verbose: bool = False) -> None:
        config_dump = self.parse_config_dump(self._record.sensor_config_dump)
        print("=== Session info " + "=" * 43)
        for k, v in config_dump.items():
            print(f"{k:30} {v} ")
        print("=" * 60)
        print()

        if not verbose:
            return

        record = self._record
        print("Mode:", record.mode.name.lower())
        print()
        print(record.sensor_config)
        print()
        print("Session info")

        for k, v in record.session_info.items():
            print("  {:.<35} {}".format(k + " ", v))

        print()
        print("Data shape:", record.data.shape)
        print("Data dtype:", record.data.dtype)
        print()
        print("Last data info (first sensor):")

        for k, v in record.data_info[-1][0].items():
            print("  {:.<35} {}".format(k + " ", v))

        ts = record.sample_times
        if ts is not None and ts.size >= 2:
            print()
            mean_dt = (ts[-1] - ts[0]) / (ts.size - 1)
            mean_f = 1 / mean_dt
            print("Mean sample rate (client side): {:.2f} Hz".format(mean_f))

        print("\n")

        print("Module (processing) key:", record.module_key)

        if record.processing_config_dump is None:
            print("No processing config dump")
        else:
            print("Processing config dump")
            for k, v in json.loads(record.processing_config_dump).items():
                print("  {:.<35} {}".format(k + " ", v))

        print("\n")

        environtment_a111 = get_environment(record)

        for k, v in environtment_a111.items():
            print("{:.<37} {}".format(k + " ", v))

        if record.note:
            print()
            print("Note: " + str(record.note))

    @staticmethod
    def parse_config_dump(config: str) -> t.Any:
        context = {"null": None, "true": True, "false": False}
        return eval(config, context)


class A121RecordTableConverter(TableConverter):
    def __init__(self, record: a121.Record) -> None:
        self._record = record

    def _results_of_sensor_id(self, sensor_id: int) -> list[a121.Result]:
        return [
            ext_result[sensor_id]
            for ext_result_group in self._record.extended_results
            for ext_result in ext_result_group
            if sensor_id in ext_result
        ]

    def _unique_sensor_configs_of_sensor_id(self, sensor_id: int) -> list[a121.SensorConfig]:
        # FIXME: this is not a `set` as SensorConfig is not hash-able
        sensor_configs = [
            sensor_config
            for _, sid, sensor_config in _core.utils.iterate_extended_structure(
                self._record.session_config.groups
            )
            if sid == sensor_id
        ]
        unique_sensor_configs = []
        for sensor_config in sensor_configs:
            if sensor_config not in unique_sensor_configs:
                unique_sensor_configs.append(sensor_config)
        return unique_sensor_configs

    def _convert_single_sensor_config(
        self,
        sensor: int,
    ) -> npt.NDArray[t.Any]:
        """This function handles the case where the sensor at "sensor ID" is configured
        with a single unique `SensorConfig`, possibly in multiple groups.

        :param sensor: The sensor ID.
        :returns: 2D NDArray of cell values.
        """
        return np.array(
            [
                [self.format_cell_value(v) for v in result.frame.flatten()]
                for result in self._results_of_sensor_id(sensor)
            ]
        )

    def _convert_multiple_sensor_config(self, sensor: int) -> npt.NDArray[t.Any]:
        """
        This function handles the case where the sensor at "sensor ID" is configured
        with a multiple unique `SensorConfig` across groups.

        :param sensor: The sensor ID.
        :returns: 2D NDArray of cell values.
        """
        raise NotImplementedError(
            "This record contains data where a single sensor has multiple configuration through\n"
            + "the use of groups. Exporting this kind of record is not possible at the moment.\n"
            + "\n"
            + "If this is a feature that you are interested in, please get in contact with us!"
        )

    def convert(self, sensor: int) -> npt.NDArray[t.Any]:
        """Converts data of a single sensor

        :param sensor: The sensor index
        :returns: 2D NDArray of cell values.
        """
        unique_sensor_configs = self._unique_sensor_configs_of_sensor_id(sensor)

        if len(unique_sensor_configs) == 1:
            return self._convert_single_sensor_config(sensor)

        if len(unique_sensor_configs) > 1:
            return self._convert_multiple_sensor_config(sensor)

        raise ValueError(f"This record contains no data of sensor with id = {sensor}")

    def _get_metadata_rows_single_sensor_config(self, sensor: int) -> list[npt.NDArray[t.Any]]:
        (sensor_config,) = self._unique_sensor_configs_of_sensor_id(sensor)
        (metadata,) = (
            meta
            for _, sid, meta in _core.utils.iterate_extended_structure(
                self._record.extended_metadata
            )
            if sid == sensor
        )
        depths, _ = algo.get_distances_m(sensor_config, metadata)

        sweep_numbers = np.repeat(
            range(sensor_config.sweeps_per_frame), repeats=sensor_config.num_points
        ).astype(int)
        depths_header = np.tile(depths, sensor_config.sweeps_per_frame)
        return [sweep_numbers, depths_header]

    def _get_metadata_rows_multiple_sensor_config(self, sensor: int) -> list[npt.NDArray[t.Any]]:
        raise NotImplementedError(
            "This record contains data where a single sensor has multiple configuration through\n"
            + "the use of groups. Exporting this kind of record is not possible at the moment.\n"
            + "\n"
            + "If this is a feature that you are interested in, please get in contact with us!"
        )

    def get_metadata_rows(self, sensor: int) -> list[npt.NDArray[t.Any]]:
        unique_sensor_configs = self._unique_sensor_configs_of_sensor_id(sensor)

        if len(unique_sensor_configs) == 1:
            return self._get_metadata_rows_single_sensor_config(sensor)
        else:
            return self._get_metadata_rows_multiple_sensor_config(sensor)

    def print_information(self, verbose: bool = False) -> None:
        extended = self._record.session_config.extended

        print("=== Session config " + "=" * 41)
        print(self._record.session_config)

        if not verbose:
            print("=" * 60)
            return

        print("=== Meta data " + "=" * 46)
        pprint(self._record.extended_metadata if extended else self._record.metadata)
        print("=== Server info " + "=" * 44)
        pprint(self._record.server_info)
        print("=== Client info " + "=" * 44)
        pprint(self._record.client_info)

        environtment_a121 = get_environment(self._record)

        for k, v in environtment_a121.items():
            print("{:.<37} {}".format(k + " ", v))

        print("=" * 60)


def get_environment(
    record: Union[et.a111.recording.Record, a121.Record]
) -> dict[str, Optional[str]]:
    if isinstance(record, et.a111.recording.Record):
        environment_dict = {
            "RSS version": record.rss_version,
            "acconeer.exptool library version": record.lib_version,
            "Timestamp": record.timestamp,
        }
        return environment_dict

    elif isinstance(record, a121.Record):
        environment_dict = {
            "RSS version": record.server_info.rss_version,
            "Exptool version": record.lib_version,
            "Number of frames": str(record.num_frames),
            "Timestamp": record.timestamp,
            "UUID": record.uuid,
        }
        return environment_dict
    else:
        raise TypeError(
            f"Passed record ({record}) was of unexpected type."
            f" actual {type(record)}, expected et.a111.recording.Record or a121.Record"
        )


def _check_files(
    input_file: Path, output_file: Union[Path, None], force: bool
) -> Tuple[bool, str, Path, str, str]:
    files_ok = True
    exit_text = ""
    to_csv_sep = ","
    output_suffix = (
        ".xlsx" if output_file is None or output_file.suffix == "" else output_file.suffix
    )

    if output_suffix == ".tsv":
        to_csv_sep = "\t"
    output_stem = Path(input_file.stem if output_file is None else output_file.stem)
    output_stem = input_file.stem if output_stem is None else output_stem
    new_output_file = output_stem.with_suffix(output_suffix)

    if not os.path.exists(input_file):
        exit_text = str(f'The input file ("{input_file}") can not be found.')
        files_ok = False

    if os.path.exists(new_output_file) and not force:
        exit_text_0 = str(f'The output file ("{output_file}") already exists.')
        exit_text_1 = str(
            'Overwrite existing file with "-f" or give different name for output file.'
        )
        exit_text = exit_text_0 + "\n" + exit_text_1
        files_ok = False

    return files_ok, exit_text, output_stem, output_suffix, to_csv_sep


def load_file(input_file: str) -> tuple[Union[et.a111.recording.Record, a121.Record], str]:
    try:
        return a121.load_record(input_file), "a121"
    except Exception:
        pass

    try:
        return et.a111.recording.load(input_file), "a111"
    except Exception:
        pass

    raise Exception("The specified file was neither A111 or A121. Cannot load.")


def get_default_sensor_id_or_index(namespace: argparse.Namespace, generation: str) -> int:
    try:
        return int(namespace.sensor)
    except AttributeError:
        return 1 if generation == "a121" else 0


def configs_as_dataframe(session_config: a121.SessionConfig) -> pd.DataFrame:
    # Create DataFrames from session configurations
    df_config = pd.DataFrame()
    sensor_config = session_config.sensor_config
    update_rate = "Max" if session_config.update_rate is None else session_config.update_rate
    frame_rate = "Max" if sensor_config.frame_rate is None else sensor_config.frame_rate
    sweep_rate = "Max" if sensor_config.sweep_rate is None else sensor_config.sweep_rate
    configs = {
        "extended": session_config.extended,
        "update_rate": update_rate,
        "sweep_rate": sweep_rate,
        "frame_rate": frame_rate,
        "sensor_id": session_config.sensor_id,
        "continuous_sweep_mode": sensor_config.continuous_sweep_mode,
        "double_buffering": sensor_config.double_buffering,
        "inter_frame_idle_state": sensor_config.inter_frame_idle_state,
        "inter_sweep_idle_state": sensor_config.inter_sweep_idle_state,
        "sweeps_per_frame": sensor_config.sweeps_per_frame,
        "start_point": sensor_config.subsweep.start_point,
        "num_points": sensor_config.subsweep.num_points,
        "step_length": sensor_config.subsweep.step_length,
        "profile": sensor_config.subsweep.profile,
        "hwaas": sensor_config.subsweep.hwaas,
        "receiver_gain": sensor_config.subsweep.receiver_gain,
        "enable_tx": sensor_config.subsweep.enable_tx,
        "enable_loopback": sensor_config.subsweep.enable_loopback,
        "phase_enhancement": sensor_config.subsweep.phase_enhancement,
        "prf": sensor_config.subsweep.prf,
    }
    df_config = pd.DataFrame(configs.items())
    return df_config


def get_processed_data(h5_file: h5py.File) -> Tuple[pd.DataFrame, pd.DataFrame]:
    app_key = h5_file["algo/key"][()].decode()
    supported_apps = ["breathing", "presence_detector", "surface_velocity"]

    df_app_config = pd.DataFrame()
    load_algo_and_client = {
        "breathing": get_processed_data_breathing,
        "presence_detector": get_processed_data_presence,
        "surface_velocity": get_processed_data_surface_velocity,
    }
    if app_key in supported_apps:
        df_processed_data, df_app_config = load_algo_and_client[app_key](h5_file)
    else:
        df_processed_data = pd.DataFrame()
    return df_processed_data, df_app_config


def get_processed_data_breathing(h5_file: h5py.File) -> Tuple[pd.DataFrame, pd.DataFrame]:
    processed_data_list = []
    sensor_id, ref_app_config = breathing._ref_app._load_algo_data(h5_file["algo"])

    # Create DataFrames from dictionaries
    df_sensor_id = pd.DataFrame(({"sensor_id": sensor_id}).items())
    df_config = pd.DataFrame([[k, v] for k, v in ref_app_config.to_dict().items()])

    # Concatenate along columns
    df_algo_data = pd.concat([df_sensor_id, df_config], axis=0, ignore_index=True)

    # Client preparation
    record = H5Record(h5_file)
    client = _ReplayingClient(record, realtime_replay=False)
    num_frames = record.num_frames
    ref_app = breathing.RefApp(client=client, sensor_id=sensor_id, ref_app_config=ref_app_config)
    ref_app.start()

    try:
        for idx in range(record.num_frames):
            processed_data = ref_app.get_next()

            # Put the result in row
            processed_data_row = breathing_result_as_row(processed_data=processed_data)
            processed_data_list.append(processed_data_row)

            # Print progressing time every 5%
            print(f"... {idx / num_frames:.0%}") if (idx % int(0.05 * num_frames)) == 0 else None

    except KeyboardInterrupt:
        print("Conversion aborted")
    else:
        print("Processing data is finished. . .")

    transposed_processed_data_list = [list(row) for row in zip(*processed_data_list)]
    processed_data_as_dataframe = {
        "rate": transposed_processed_data_list[0],
        "motion": transposed_processed_data_list[1],
        "presence_dist": transposed_processed_data_list[2],
    }
    ref_app.stop()
    client.close()
    print("Disconnecting...")

    df_processed_data = pd.DataFrame(processed_data_as_dataframe)
    return df_processed_data, df_algo_data


def get_processed_data_surface_velocity(h5_file: h5py.File) -> Tuple[pd.DataFrame, pd.DataFrame]:
    processed_data_list = []
    sensor_id, ExampleAppConfig = surface_velocity._example_app._load_algo_data(h5_file["algo"])

    # Create DataFrames from dictionaries
    df_sensor_id = pd.DataFrame(({"sensor_id": sensor_id}).items())
    df_config = pd.DataFrame([[k, v] for k, v in ExampleAppConfig.to_dict().items()])

    # Concatenate along columns
    df_algo_data = pd.concat([df_sensor_id, df_config], axis=0, ignore_index=True)

    # Client preparation
    record = H5Record(h5_file)
    client = _ReplayingClient(record, realtime_replay=False)
    num_frames = record.num_frames

    example_app = surface_velocity.ExampleApp(
        client=client,
        sensor_id=int(sensor_id),
        example_app_config=ExampleAppConfig,
    )
    example_app.start()

    try:
        for idx in range(record.num_frames):
            processed_data = example_app.get_next()

            # Put the result in row
            processed_data_row = surface_velocity_result_as_row(processed_data=processed_data)
            processed_data_list.append(processed_data_row)

            # Print progressing time every 5%
            print(f"... {idx / num_frames:.0%}") if (idx % int(0.05 * num_frames)) == 0 else None

    except KeyboardInterrupt:
        print("Conversion aborted")
    else:
        print("Processing data is finished. . .")

    example_app.stop()
    client.close()
    print("Disconnecting...")

    transposed_processed_data_list = [list(row) for row in zip(*processed_data_list)]
    processed_data_as_dataframe = {
        "estimated_velocity": transposed_processed_data_list[0],
        "distance": transposed_processed_data_list[1],
    }

    df_processed_data = pd.DataFrame(processed_data_as_dataframe)
    return df_processed_data, df_algo_data


def get_processed_data_presence(h5_file: h5py.File) -> Tuple[pd.DataFrame, pd.DataFrame]:
    processed_data_list = []
    sensor_id, detector_config, detector_context = presence._detector._load_algo_data(
        h5_file["algo"]
    )

    # Create DataFrames from dictionaries
    df_sensor_id = pd.DataFrame(({"sensor_id": sensor_id}).items())
    df_config = pd.DataFrame([[k, v] for k, v in detector_config.to_dict().items()])

    # Concatenate along columns
    df_algo_data = pd.concat([df_sensor_id, df_config], axis=0, ignore_index=True)

    # Client preparation
    record = H5Record(h5_file)
    client = _ReplayingClient(record, realtime_replay=False)
    num_frames = record.num_frames
    detector = presence.Detector(
        client=client,
        sensor_id=int(sensor_id),
        detector_config=detector_config,
        detector_context=detector_context,
    )
    detector.start()

    try:
        for idx in range(record.num_frames):
            processed_data = detector.get_next()

            # Put the result in row
            processed_data_row = presence_result_as_row(processed_data=processed_data)
            processed_data_list.append(processed_data_row)

            # Print progressing time every 5%
            print(f"... {idx / num_frames:.0%}") if (idx % int(0.05 * num_frames)) == 0 else None

    except KeyboardInterrupt:
        print("Conversion aborted")
    else:
        print("Processing data is finished. . .")

    detector.stop()
    client.close()
    print("Disconnecting...")

    transposed_processed_data_list = [list(row) for row in zip(*processed_data_list)]
    processed_data_as_dataframe = {
        "Presence": transposed_processed_data_list[0],
        f"Intra_presence_score_(threshold_{detector_config.intra_detection_threshold:.1f})": transposed_processed_data_list[
            1
        ],
        f"Inter_presence_score_(threshold_{detector_config.inter_detection_threshold:.1f})": transposed_processed_data_list[
            2
        ],
        "Presence_distance": transposed_processed_data_list[3],
    }

    df_processed_data = pd.DataFrame(processed_data_as_dataframe)

    return df_processed_data, df_algo_data


def breathing_result_as_row(processed_data: breathing.RefAppResult) -> list[t.Any]:
    no_result = "None"
    rate = (
        no_result
        if processed_data.breathing_result is None
        or processed_data.breathing_result.breathing_rate is None
        else f"{processed_data.breathing_result.breathing_rate:0.2f}"
    )
    motion = (
        no_result
        if processed_data.breathing_result is None
        else f"{processed_data.breathing_result.extra_result.breathing_motion[-1]:0.2f}"
    )
    presence_dist = (
        no_result
        if not processed_data.presence_result.presence_detected
        else f"{processed_data.presence_result.presence_distance:0.2f}"
    )

    return [rate, motion, presence_dist]


def surface_velocity_result_as_row(
    processed_data: surface_velocity.ExampleAppResult
) -> list[t.Any]:
    velocity = f"{processed_data.velocity :.3f}"
    distance_m = f"{processed_data.distance_m :.3f} m"

    return [velocity, distance_m]


def presence_result_as_row(processed_data: presence.DetectorResult) -> list[t.Any]:
    presence_detected = "Presence!" if processed_data.presence_detected else "None"
    intra_presence_score = f"{processed_data.intra_presence_score:.3f}"
    inter_presence_score = f"{processed_data.inter_presence_score:.3f}"
    presence_dist = f"{processed_data.presence_distance:.3f} m"

    return [presence_detected, intra_presence_score, inter_presence_score, presence_dist]


def main() -> None:
    parser = ConvertToCsvArgumentParser()
    args = parser.parse_args()

    # File checking and formatting from args
    files_ok, exit_text, output_stem, output_suffix, to_csv_sep = _check_files(
        args.input_file, args.output_file, args.force
    )
    input_file = args.input_file
    if not (files_ok):
        print(exit_text)
        exit(1)
    print(f"Reading from {input_file!r} ... \n")
    record, generation = load_file(input_file)
    sensor = get_default_sensor_id_or_index(args, generation)
    table_converter = TableConverter.from_record(record)
    try:
        data_table = table_converter.convert(sensor=sensor)
    except Exception as e:
        print(e)
        exit(1)

    table_converter.print_information(verbose=args.verbose)
    print()

    if args.sweep_as_column:
        data_table = data_table.T

    # Create a Pandas DataFrame from the data
    dict_excel_file = {"Sparse IQ data": pd.DataFrame(data_table)}

    # Create a Pandas DataFrame from the environtment
    record_environtment = get_environment(record)
    dict_excel_file["Environtment"] = pd.DataFrame(record_environtment.items())

    if isinstance(record, a121.Record):
        # Add configurations in excel
        df_config = configs_as_dataframe(record.session_config)
        dict_excel_file["Configurations"] = df_config

    # Create a Pandas DataFrame from processed data
    h5_file = h5py.File(str(input_file))
    df_processed_data, df_app_config = get_processed_data(h5_file)
    dict_excel_file["Application configurations"] = df_app_config
    dict_excel_file["Processed data"] = df_processed_data

    h5_file.close()
    # Save the DataFrame to a CSV or excel file
    if output_suffix == ".xlsx":
        output_file = output_stem.with_suffix(output_suffix)
        # Write each DataFrame to a separate sheet using to_excel
        # Default example data frame is written as below
        with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
            # Write each DataFrame to a separate sheet
            for key, value in dict_excel_file.items():
                pd.DataFrame(value).to_excel(
                    writer, sheet_name=key, index_label="Index", header=True
                )

    if output_suffix == ".csv" or output_suffix == ".tsv":
        # Write each DataFrame to a separate sheet using to_csv
        for key, value in dict_excel_file.items():
            pd.DataFrame(value).to_csv(
                Path(str(output_stem) + "_" + key + output_suffix),
                sep=to_csv_sep,
                index_label="Index",
            )

    print("Success!")


if __name__ == "__main__":
    main()
