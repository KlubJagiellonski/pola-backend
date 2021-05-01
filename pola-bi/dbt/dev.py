#!/usr/bin/env python

import argparse
import json
import os
import shlex
import subprocess
from typing import Dict

from environ import environ

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def print_env_vars(all_env_vars: Dict[str, str]) -> None:
    for key, value in all_env_vars.items():
        print(f'export {shlex.quote(key)}={shlex.quote(value)}')


def db_url_to_env_var(database_url: str, prefix: str) -> Dict[str, str]:
    db_config = environ.Env.db_url_config(database_url)
    db_config_env_var = {
        f"{prefix}_HOST": str(db_config['HOST']),
        f"{prefix}_PORT": str(db_config['PORT'] or 5432),
        f"{prefix}_USER": str(db_config['USER']),
        f"{prefix}_PASS": str(db_config['PASSWORD']),
        f"{prefix}_DB_NAME": str(db_config['NAME']),
    }
    return db_config_env_var


def load_database_url(environment: str) -> str:
    if environment == 'staging':
        return fetch_database_url_from_heroku(app_name='pola-staging')
    elif environment == 'prod':
        return fetch_database_url_from_heroku(app_name='pola-app')
    elif environment == 'local':
        return "postgres://pola_app:pola_app@localhost/pola_app"
    raise SystemExit(f"Unknown environment:{environment}")


def fetch_database_url_from_heroku(app_name: str) -> str:
    env_var_json = fetch_heroku_env_vars(app_name)
    if 'DATABASE_URL' not in env_var_json:
        raise SystemExit('The database configuration could not be found. Variable DATABASE_URL is not defined.')
    database_url = env_var_json['DATABASE_URL']
    return database_url


def fetch_heroku_env_vars(app_name: str) -> Dict[str, str]:
    return json.loads(subprocess.check_output(['heroku', 'config', '--app', app_name, '--json']))


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch credentials to database access.')
    parser.add_argument(
        '--environment', metavar='ENV', choices=('local', 'prod', 'staging'), help='Environment', default='local'
    )
    return parser


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    environment = args.environment

    database_url = load_database_url(environment)
    db_config_env_var = db_url_to_env_var(database_url, prefix="POLA_APP")
    all_env_vars = {
        **db_config_env_var,
        'POLA_APP_SCHEMA': 'public',
        'DATABASE_URL': database_url,
        'DBT_PROFILES_DIR': os.path.join(CURRENT_DIR, 'profile'),
    }

    print_env_vars(all_env_vars)

    print("# To load variable, run:")
    print("# Local: eval $(python dev.py)")
    print("# Prod: eval $(python dev.py --environment prod)")
    print("# Staging: eval $(python dev.py --environment staging)")


if __name__ == '__main__':
    main()
