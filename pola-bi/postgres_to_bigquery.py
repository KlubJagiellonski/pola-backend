#!/usr/bin/env python3
import argparse
import csv
import logging
import os
import urllib.parse as urlparse
from concurrent.futures import ThreadPoolExecutor
from tempfile import NamedTemporaryFile

import psycopg2
from google.cloud import bigquery, storage

EXCLUDED_COLUMNS = ['password']


def setup_logging(verbose):
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')


def get_columns(cursor, table_name):
    """
    Retrieve all column names from a table, excluding sensitive columns.
    """
    exclude_clause = " AND ".join("column_name != %s" for column in EXCLUDED_COLUMNS)
    query = f"""
    SELECT column_name FROM information_schema.columns
    WHERE table_name = %s AND {exclude_clause};
    """
    cursor.execute(query, [table_name] + EXCLUDED_COLUMNS)
    return [row[0] for row in cursor.fetchall()]


def export_to_file(connection_info, table_name, csv_path, verbose):
    setup_logging(verbose)
    logging.info('Start exporting data from %s table to %s file', table_name, csv_path)
    with (
        psycopg2.connect(**connection_info) as conn,
        conn.cursor() as cursor,
        open(csv_path, mode='w', newline='') as file,
    ):
        columns = get_columns(cursor, table_name)
        if not columns:
            raise ValueError(f"No columns found for table {table_name}.")
        query = 'SELECT "' + '", "'.join(columns) + f'" FROM "{table_name}"'
        cursor.execute(query)
        writer = csv.writer(file)
        writer.writerow(columns)
        rows_exported = 0
        for row in cursor:
            writer.writerow(row)
            rows_exported = rows_exported + 1

    file_size = os.path.getsize(csv_path)
    logging.info(f"Exported {rows_exported} rows ({file_size} bytes).")


def upload_to_gcs(source_file_path, destination_url, verbose):
    setup_logging(verbose)

    # Parse the destination URL
    if not destination_url.startswith('gs://'):
        raise ValueError(f"URL must start with 'gs://'. Current url: {destination_url}")

    path_parts = destination_url[len('gs://') :].split('/', 1)
    if len(path_parts) < 2:
        raise ValueError(f"URL must include a bucket name and a destination path.  Current url: {destination_url}")

    bucket_name, destination_blob_name = path_parts[0], path_parts[1]

    # Get file size for logging
    file_size = os.path.getsize(source_file_path)
    logging.info(f"Start uploading file: {source_file_path} ({file_size} bytes).")

    # Create a storage client and upload the file
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

    logging.info(f"Uploaded file to {destination_blob_name} in bucket {bucket_name}.")


def load_to_bigquery(gcs_uri, dataset_id, table_id, verbose):
    setup_logging(verbose)
    logging.info(f"Start loading data into BigQuery table {dataset_id}.{table_id} from {gcs_uri}.")
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job_config.allow_quoted_newlines = True

    job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
    job.result()
    logging.info(f"Loaded data. Job ID: {job.job_id}")


def parse_database_url(database_url):
    result = urlparse.urlparse(database_url)
    return {
        "database": result.path[1:],
        "user": result.username,
        "password": result.password,
        "host": result.hostname,
        "port": result.port,
    }


def all_operations(connection_info, table_names, dataset_id, staging_url, verbose):
    setup_logging(verbose)
    logging.info("Start replication for tables: %s", table_names)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(single_table_workflow, connection_info, table_name, dataset_id, staging_url, verbose)
            for table_name in table_names
        ]
        for future in futures:
            future.result()


def single_table_workflow(connection_info, table_name, dataset_id, staging_url, verbose):
    with NamedTemporaryFile(delete=True, suffix='.csv', mode='w+') as temp_file:
        csv_file_path = temp_file.name
        export_to_file(connection_info, table_name, csv_file_path, verbose)
        gcs_uri = append_file_to_url(staging_url, f'{table_name}.csv')
        upload_to_gcs(csv_file_path, gcs_uri, verbose)
        load_to_bigquery(gcs_uri, dataset_id, table_name, verbose)


def setup_arg_parser():
    parser = argparse.ArgumentParser(description="Manage data transfer between PostgreSQL, GCS, and BigQuery.")
    parser.add_argument("--verbose", action='store_true', help="Enable verbose logging")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Subcommand to run')

    export_parser = subparsers.add_parser('export', help='Export data to local file')
    export_parser.add_argument("--database-url", required=True, help="Complete PostgreSQL database URL")
    export_parser.add_argument(
        "--table-names", required=True, help="Comma-separated list of PostgreSQL table names to export"
    )
    export_parser.add_argument("--target-path", required=True, help="Path to save the CSV file")

    upload_parser = subparsers.add_parser('upload', help='Upload files to GCS')
    upload_parser.add_argument("--source-path", required=True, help="Local file path to upload")
    upload_parser.add_argument("--destination-url", required=True, help="Destination blob name in GCS")

    load_parser = subparsers.add_parser('load', help='Load files from GCS to BigQuery')
    load_parser.add_argument("--source-url", required=True, help="GCS URI of the file to load")
    load_parser.add_argument("--dataset-id", required=True, help="BigQuery dataset ID")
    load_parser.add_argument("--table-id", required=True, help="BigQuery table ID")

    all_parser = subparsers.add_parser('all', help='Execute all steps')
    all_parser.add_argument("--database-url", required=True, help="Complete PostgreSQL database URL")
    all_parser.add_argument("--table-names", required=True, help="Comma-separated list of table names")
    all_parser.add_argument(
        "--staging-url", required=True, help="Staging URL in GCS bucket where CSV files will be stored"
    )
    all_parser.add_argument("--dataset-id", required=True, help="BigQuery dataset ID")

    return parser


def append_file_to_url(url, file_name):
    """
    Appends a file name to a URL, ensuring correct formatting.

    Parameters:
    - url (str): The base URL to which the file name will be appended.
    - file_name (str): The file name to append to the URL.

    Returns:
    - str: The full URL with the file name appended.
    """
    # Ensure the URL ends with a slash
    if not url.endswith('/'):
        url += '/'
    return url + file_name


def main():
    args = setup_arg_parser().parse_args()
    verbose = args.verbose
    connection_info = parse_database_url(args.database_url)
    if args.command == 'export':
        for table_name in args.table_names.split(','):
            export_to_file(connection_info, table_name, args.target_path, verbose)
    elif args.command == 'upload':
        upload_to_gcs(args.source_path, args.destinatio_url, verbose)
    elif args.command == 'load':
        load_to_bigquery(args.source_url, args.dataset_id, args.table_id, verbose)
    elif args.command == 'all':
        table_names = [t.strip() for t in args.table_names.split(',')]
        all_operations(connection_info, table_names, args.dataset_id, args.staging_url, verbose)


if __name__ == "__main__":
    main()
