#!/usr/bin/env python

import argparse
import json
import pathlib
import shlex
import subprocess

current_directory = pathlib.Path(__file__).resolve().parent


def get_model_list():
    manifest_path = current_directory / "dbt" / "target" / "manifest.json"
    manifest_content = json.loads(manifest_path.read_text())
    return [node['name'] for node_key, node in manifest_content['nodes'].items() if node['resource_type'] == 'model']


def save_sql_to_csv_file(table_name: str, output_file: pathlib.Path):
    abs_output_path = output_file.resolve()
    command = [
        "docker",
        "run",
        "-e",
        "PGHOST",
        "-e",
        "PGPORT",
        "-e",
        "PGUSER",
        "-e",
        "PGPASSWORD",
        "-e",
        "PGDATABASE",
        "-v",
        f"{abs_output_path.parent}:{abs_output_path.parent}",
        "--network",
        "pola-backend_default",
        "postgres:13.1",
    ]
    command += ["psql", fr"--command=\copy {table_name} to '{abs_output_path}' with csv header"]
    print("Executing command: ", " ".join([shlex.quote(c) for c in command]))
    subprocess.check_call(command, timeout=30)
    print()


def get_parser():
    parser = argparse.ArgumentParser(__name__)
    parser.add_argument("output_directory")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    output_directory = pathlib.Path(args.output_directory)
    if not output_directory.exists():
        raise SystemExit(f"Director not exists: {output_directory}")
    if not output_directory.is_dir():
        raise SystemExit(f"Path is not directory: {output_directory}")
    for model_name in get_model_list():
        output_file_path = output_directory / f"{model_name}.csv"
        save_sql_to_csv_file(model_name, output_file_path)


if __name__ == "__main__":
    main()
