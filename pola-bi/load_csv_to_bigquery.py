#!/usr/bin/env python

import argparse
import os
import pathlib
import re
import shlex
import subprocess
import tempfile
import textwrap

TABLE_NAME_PATTERN = re.compile(r'[\W_]+')
ADC_ENV = 'GOOGLE_APPLICATION_CREDENTIALS'


def get_parser():
    parser = argparse.ArgumentParser(__name__)
    parser.add_argument("input_directory")
    parser.add_argument("dataset")
    return parser


def load_csv_to_bigquery(self, dataset_name: str, csv_file_path: pathlib.Path):
    with tempfile.NamedTemporaryFile() as tmpfile:
        table_name = TABLE_NAME_PATTERN.sub("-", csv_file_path.name)
        command = ["docker", "run", "-v", f"{csv_file_path.resolve()}:{csv_file_path.resolve()}"]
        if ADC_ENV in os.environ and pathlib.Path(os.environ[ADC_ENV]).exists():
            tmpfile.write(
                textwrap.dedent(
                    """
            [auth]
            credential_file_override = /sa.json
            """
                ).encode()
            )
            command += ["-v", f"{os.environ[ADC_ENV]}:/sa.json", "-e", f"{ADC_ENV}=/sa.json"]
        command += ["google/cloud-sdk:latest"]
        command += [
            "bq",
            "load",
            "--source_format=CSV",
            "--replace=true",
            "--autodetect",
            f"{dataset_name}.{table_name}",
            str(csv_file_path),
        ]
        print("Executing command: ", " ".join([shlex.quote(c) for c in command]))
        subprocess.check_call(command, timeout=30)


def main():
    parser = get_parser()
    args = parser.parse_args()
    input_directory = pathlib.Path(args.input_directory)
    dataset_name = args.dataset
    if not input_directory.exists():
        raise SystemExit(f"Director not exists: {input_directory}")
    if not input_directory.is_dir():
        raise SystemExit(f"Path is not directory: {input_directory}")

    for csv_file_path in input_directory.glob("*.csv"):
        load_csv_to_bigquery(dataset_name, csv_file_path)


if __name__ == '__main__':
    main()
