#!/usr/bin/env python3
import contextlib
import os
import subprocess

if __name__ not in ("__main__", "__mp_main__"):
    raise SystemExit(
        "This file is intended to be executed as an executable program. You cannot use it as a module."
        f"To run this script, run the ./{__file__} command"
    )

IS_GITHUB_ACTION = os.environ.get('GITHUB_ACTIONS', 'false').lower() == 'true'


class Terminal:
    BOLD = '\033[1m'
    RESET = '\033[0m'


@contextlib.contextmanager
def github_action_group(name: str) -> None:
    try:
        if IS_GITHUB_ACTION:
            print(f'::group::{name}')
        else:
            print(f":::{Terminal.BOLD}{name}{Terminal.RESET}:::")
        yield
    finally:
        if IS_GITHUB_ACTION:
            print("::endgroup::")
        else:
            print(f":::{Terminal.BOLD}--END GROUP--{Terminal.RESET}:::")


def main():
    image_names = subprocess.check_output(['docker', 'compose', 'config', '--images']).decode().strip().splitlines()
    image_names = [image_name for image_name in image_names if "pola" not in image_name]
    for image_name in image_names:
        with github_action_group(f"Pulling {image_name!r} image"):
            subprocess.run(['docker', 'pull', image_name], check=True)


main()
