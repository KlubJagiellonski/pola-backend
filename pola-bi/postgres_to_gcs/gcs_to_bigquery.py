#!/usr/bin/env python3
import argparse
import json
import logging
import shlex
import subprocess
from tempfile import NamedTemporaryFile

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


def execute_verbose(command, **kwargs):
    log.info("Executing command: %s", shlex.join(command))
    subprocess.run(command, check=True, **kwargs)


SCHEMAS = {
    'product_product': [
        {"mode": "NULLABLE", "name": "id", "type": "INTEGER"},
        {"mode": "NULLABLE", "name": "name", "type": "STRING"},
        {
            "mode": "NULLABLE",
            "name": "code",
            # Change to STRING from INTEGER as some values are not INT64 (length > 19)
            "type": "STRING",
        },
        {"mode": "NULLABLE", "name": "created", "type": "TIMESTAMP"},
        {"mode": "NULLABLE", "name": "ilim_queried_at", "type": "TIMESTAMP"},
        {"mode": "NULLABLE", "name": "query_count", "type": "INTEGER"},
        {"mode": "NULLABLE", "name": "ai_pics_count", "type": "INTEGER"},
        {"mode": "NULLABLE", "name": "brand_id", "type": "INTEGER"},
        {"mode": "NULLABLE", "name": "company_id", "type": "INTEGER"},
        {"mode": "NULLABLE", "name": "modified", "type": "TIMESTAMP"},
        {"mode": "NULLABLE", "name": "gpc_brick_id", "type": "INTEGER"},
        {"mode": "NULLABLE", "name": "gs1_last_response", "type": "STRING"},
    ]
}


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch credentials to database access.')
    parser.add_argument('--source')
    parser.add_argument('--target-location')
    parser.add_argument('--target-dataset')

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    source = args.source
    target_location = args.target_location
    target_dataset = args.target_dataset

    csv_files = (
        subprocess.check_output(['gcloud', 'storage', 'ls', '--recursive', f'{source}/**/*.csv']).decode().splitlines()
    )

    for no, csv_file in enumerate(csv_files, start=1):
        log.info("Loading file %s (%d/%d)", csv_file, no, len(csv_files))
        table_name = csv_file.split('/')[-1].split('.')[0]

        with NamedTemporaryFile() as f:
            # Prepare the bq command
            bq_command = [
                'bq',
                'load',
                f'--location={target_location}',
                '--allow_quoted_newlines=true',
                '--autodetect',
                '--replace',
                '--source_format=CSV',
            ]

            # Append the custom schema if it exists
            schema = SCHEMAS.get(table_name)
            if schema:
                f.write(json.dumps(schema).encode())
                f.seek(0)
                schema_file_path = f.name
                bq_command.append(f'--schema={schema_file_path}')

            # Append the target table and the source CSV file (positional arguments)
            bq_command.extend([f'{target_dataset}.{table_name}', csv_file])
            execute_verbose(bq_command)


if __name__ == "__main__":
    main()
