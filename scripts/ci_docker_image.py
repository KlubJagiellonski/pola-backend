#!/usr/bin/env python

import argparse
import difflib
import itertools
import os
import shlex
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

PREPARE_BUILDX_CACHE = os.environ.get('PREPARE_BUILDX_CACHE', 'false').lower() == 'true'
print("PREPARE_BUILDX_CACHE =", PREPARE_BUILDX_CACHE)

GITHUB_REPOSITORY = os.environ.get('GITHUB_REPOSITORY', 'KlubJagiellonski/pola-backend')
print('GITHUB_REPOSITORY =', GITHUB_REPOSITORY)

GITHUB_ORGANIZATION = os.environ.get('GITHUB_ORGANIZATION', 'KlubJagiellonski')
print('GITHUB_ORGANIZATION =', GITHUB_ORGANIZATION)

CONTAINER_REGISTRY = os.environ.get('CONTAINER_REGISTRY', f'ghcr.io/{GITHUB_REPOSITORY}').lower()
print('CONTAINER_REGISTRY =', CONTAINER_REGISTRY)

DJANGO_VERSION_PROD = next(
    line.split("=")[2]
    for line in (ROOT_DIR / "dependencies" / "constraints-production.txt").read_text().splitlines()
    if line.lower().startswith('django==')
)
DJANGO_VERSION = os.environ.get('DJANGO_VERSION', DJANGO_VERSION_PROD)
print('DJANGO_VERSION =', DJANGO_VERSION)

PYTHON_VERSION = os.environ.get('PYTHON_VERSION', "3.9")
print('PYTHON_VERSION =', PYTHON_VERSION)

IMAGE_TAG = os.environ.get('IMAGE_TAG', 'latest')
print('IMAGE_TAG =', IMAGE_TAG)

CI_IMAGE_NAME = f"{CONTAINER_REGISTRY}/pola-backend-{DJANGO_VERSION}-{PYTHON_VERSION}-ci"
print('CI_IMAGE_NAME =', CI_IMAGE_NAME)


def cmd_build_image(args):
    extra_build_args = []
    if PREPARE_BUILDX_CACHE:
        extra_build_args += [
            f"--cache-to=type=registry,ref={CI_IMAGE_NAME}:cache,mode=max",
            "--load",
            "--builder",
            "pola_cache",
        ]
        if subprocess.check_call(['docker', 'buildx', 'inspect', 'pola_cache']):
            subprocess.run(['docker', 'buildx', 'create', '--name', 'pola_cache'], check=True)

    cmd = [
        'docker',
        'buildx',
        'build',
        '.',
        '--pull',
        *extra_build_args,
        '--build-arg',
        f'PYTHON_VERSION={PYTHON_VERSION}',
        '--build-arg',
        f'DJANGO_VERSION={DJANGO_VERSION}',
        f"--cache-from={CI_IMAGE_NAME}:cache",
        "--file=scripts/ci-docker-image/Dockerfile",
        f"--tag={CI_IMAGE_NAME}:{IMAGE_TAG}",
    ]
    print("Executing command:  ", shlex.join(cmd))
    subprocess.run(cmd, env={**os.environ, 'DOCKER_BUILDKIT': '1'}, check=True)
    subprocess.run(['docker', 'tag', f"{CI_IMAGE_NAME}:{IMAGE_TAG}", "pola-backend_web:latest"], check=True)


def side_by_side_diff(a, b):
    cruncher = difflib.SequenceMatcher(a=a, b=b)
    a_max_length = max(len(item) for item in a)
    b_max_length = max(len(item) for item in b)

    for tag, alo, ahi, blo, bhi in cruncher.get_opcodes():
        if tag == 'replace':
            for left, right in itertools.zip_longest(a[alo:ahi], b[blo:bhi], fillvalue=''):
                print(left, end="")
                print(" " * (a_max_length - len(left)), end="")
                print("| ")
                print(right, end="")
                print(" " * (b_max_length - len(right)), end="")
                print()
        elif tag == 'delete':
            for left in a[alo:ahi]:
                print(left, end="")
                print(" " * (a_max_length - len(left)), end="")
                print("< ", end="")
                print()
        elif tag == 'insert':
            for right in b[blo:bhi]:
                print(" " * a_max_length, end="")
                print("> ", end="")
                print(right, end="")
                print()
        elif tag == 'equal':
            for left_right in a[alo:ahi]:
                print(left_right, end="")
                print(" " * (a_max_length - len(left_right)), end="")
                print("  ", end="")
                print(left_right, end="")
                print(" " * (b_max_length - len(left_right)), end="")
                print()
        else:
            raise ValueError(f'unknown tag {tag!r}')


def cmd_verify_image(args):
    current_requirements = (
        subprocess.check_output(
            ['docker', 'run', '--entrypoint', '/bin/bash', '--rm', f'{CI_IMAGE_NAME}:{IMAGE_TAG}', '-c', "pip freeze"]
        )
        .decode()
        .splitlines()
    )
    current_requirements = (d for d in current_requirements if d.strip())
    current_requirements = [d for d in current_requirements if not d.lower().startswith('"Django==')]
    current_requirements = sorted(current_requirements, key=lambda d: d.lower())

    expected_requirements = (ROOT_DIR / "dependencies" / "constraints-ci.txt").read_text().splitlines()
    expected_requirements = (d for d in expected_requirements if d.strip())
    expected_requirements = [d for d in expected_requirements if not d.lower().startswith('"Django==')]
    expected_requirements = sorted(expected_requirements, key=lambda d: d.lower())

    if current_requirements != expected_requirements:
        side_by_side_diff(current_requirements, expected_requirements)
        sys.exit(1)
    else:
        print("Dependencies identical")


def cmd_push_image(args):
    image_name = f"{CI_IMAGE_NAME}:{IMAGE_TAG}"
    print(f"Pushing image: {image_name!r}")
    subprocess.run(['docker', 'tag', 'pola-backend_web', image_name], check=True)
    subprocess.run(['docker', 'push', image_name], check=True)


def get_parser():
    parser = argparse.ArgumentParser(prog=Path(__file__).name)
    subparsers = parser.add_subparsers(dest="subcommand", metavar="COMMAND")
    subparsers.required = True

    build_image = subparsers.add_parser('build_image', help="Build image")
    build_image.set_defaults(func=cmd_build_image)

    verify_image = subparsers.add_parser('verify_image', help="Verify image")
    verify_image.set_defaults(func=cmd_verify_image)

    push_image = subparsers.add_parser('push_image', help="Push image")
    push_image.set_defaults(func=cmd_push_image)

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    args.func(args)


main()
