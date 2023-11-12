#!/usr/bin/env python

import argparse
import json
import subprocess
import sys

if __name__ not in ("__main__", "__mp_main__"):
    raise SystemExit(
        "This file is intended to be executed as an executable program. You cannot use it as a module."
        f"To run this script, run the ./{__file__} command"
    )


def get_parser():
    parser = argparse.ArgumentParser(description="Fetch preferred domain for Heroku app.")
    parser.add_argument('app_name', help="Name of heroku application")
    parser.add_argument('--all', action="store_true", help="Print all domains instead of first one only.")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    heroku_output = json.loads(subprocess.check_output(['heroku', 'domains', '--app', args.app_name, '--json']))
    domains = [d['hostname'] for d in heroku_output]
    if not domains:
        print("No domains", file=sys.stderr)
        sys.exit(1)
    if args.all:
        for d in domains:
            print(d)
    else:
        print(domains[0])


main()
