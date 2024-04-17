#!/usr/bin/env python3
import argparse
import logging
import os
import shlex
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

postgres_docker_image = "postgres:13.1"
pg_host = os.getenv('POLA_APP_HOST')
pg_port = os.getenv('POLA_APP_PORT', '5432')
pg_database = os.getenv('POLA_APP_DB_NAME')
pg_user = os.getenv('POLA_APP_USER')
pg_password = os.getenv('POLA_APP_PASS')
root_dir = Path(__file__).resolve().parent

if not all([pg_host, pg_database, pg_user, pg_password]):
    raise SystemExit("Missing required environment variables")


tables_to_export = [
    "ai_pics_aiattachment",
    "ai_pics_aipics",
    "bi_companies_by_query_group",
    "bi_companies_with_count_group",
    "bi_new_product_by_hour",
    "bi_popular_not_verified_products",
    "bi_product_by_time",
    "bi_queries_by_time",
    "bi_queries_stats_intervals",
    "bi_stats_queries_uq_users_by_week",
    "company_brand",
    "company_company",
    "gpc_brick",
    "gpc_class",
    "gpc_family",
    "gpc_segment",
    "pola_query",
    "pola_searchquery",
    "pola_stats",
    "product_product",
    "report_attachment",
    "report_report",
]


def execute_verbose(command, **kwargs):
    log.info("Executing command: %s", shlex.join(command))
    subprocess.run(command, check=True, **kwargs)


def dump_table(table_name, output_directory):
    sql_statement = fr"\COPY (SELECT * FROM {table_name}) TO '/output/{table_name}.csv' WITH CSV HEADER"
    log.info("Running SQL statement: %s", sql_statement)
    psql_command = [
        "docker",
        "run",
        "--rm",
        "-e",
        "PGHOST",
        "-e",
        "PGPORT",
        "-e",
        "PGDATABASE",
        "-e",
        "PGUSER",
        "-e",
        "PGPASSWORD",
        "-v",
        f"{output_directory}/:/output/",
        postgres_docker_image,
        "psql",
        "-c",
        sql_statement,
    ]

    # Uruchomienie polecenia
    env = {
        **os.environ,
        'PGHOST': pg_host,
        'PGPORT': pg_port,
        'PGPASSWORD': pg_password,
        'PGUSER': pg_user,
        'PGDATABASE': pg_database,
    }
    execute_verbose(psql_command, env=env)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Dump tables from PostgreSQL to CSV files.')
    parser.add_argument('--output-dir', help='Output directory', default=str(root_dir / 'output'))
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    output_dir = args.output_dir

    execute_verbose(["mkdir", "-p", output_dir])
    execute_verbose(['docker', 'pull', postgres_docker_image])

    for no, table_name in enumerate(tables_to_export, start=1):
        log.info("Exporting table %s (%s/%s)", table_name, no, len(tables_to_export))
        dump_table(table_name, output_dir)
        logging.info("")

    logging.info("Export completed successfully")


if __name__ == "__main__":
    main()
