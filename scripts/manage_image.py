#!/usr/bin/env python3

import argparse
import difflib
import itertools
import json
import logging
import os
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Konfigurujemy podstawowy logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

repo_root = Path(__file__).resolve().parent.parent

###############################################################################
# Konfiguracja dla trzech rodzajów obrazów: CI, BI, PROD
###############################################################################

DEFAULT_GITHUB_REPOSITORY = "KlubJagiellonski/pola-backend"
DEFAULT_GITHUB_ORGANIZATION = "KlubJagiellonski"

IMAGE_CONFIG = {
    "ci": {
        "dockerfile": repo_root / "scripts/ci-docker-image/Dockerfile",
        "constraints_file": repo_root / "dependencies/constraints-ci.txt",
        "local_image_name": "pola-backend_web:latest",
        "ignore_django": True,  # W CI ignorujemy Django w porównaniu constraints.
        "image_name_format": "{CONTAINER_REGISTRY}/pola-backend-{DJANGO_VERSION}-{PYTHON_VERSION}-ci",
        "pull_latest_before_build": False,
    },
    "bi": {
        "dockerfile": repo_root / "scripts/bi-docker-image/Dockerfile",
        "constraints_file": repo_root / "dependencies/constraints-bi.txt",
        "local_image_name": "pola-bi:latest",
        "ignore_django": False,
        "image_name_format": "{CONTAINER_REGISTRY}/pola-bi",
        "pull_latest_before_build": True,
    },
    "prod": {
        "dockerfile": repo_root / "scripts/prod-docker-image/Dockerfile",
        "constraints_file": repo_root / "dependencies/constraints-production.txt",
        "local_image_name": "pola-backend_prod:latest",
        "ignore_django": False,
        "image_name_format": "{CONTAINER_REGISTRY}/pola-backend",
        "pull_latest_before_build": False,
    },
}

###############################################################################
# Funkcje pomocnicze
###############################################################################


def run_command(command, capture_output=False, check=True):
    """
    Uruchamia podany command (listę argumentów) za pomocą subprocess.run.
    Loguje wywołanie, a w razie błędu zgłasza wyjątek.
    """
    logger.info("Uruchamiam polecenie: %s", shlex.join(command))
    result = subprocess.run(command, text=True, capture_output=capture_output)

    if check and result.returncode != 0:
        if capture_output:
            logger.error(
                "Polecenie nie powiodło się (kod: %d). STDOUT: %s STDERR: %s",
                result.returncode,
                result.stdout,
                result.stderr,
            )
            raise subprocess.CalledProcessError(result.returncode, command, result.stdout + "\n" + result.stderr)
        else:
            logger.error("Polecenie nie powiodło się (kod: %d). ", result.returncode)
            raise subprocess.CalledProcessError(result.returncode, command)

    return result


def docker_run(image, cmd=None, entrypoint=None, remove=True, capture_output=False, check=True):
    """
    Pomocnicza funkcja do uruchamiania `docker run`. Pozwala skrócić i uczytelnić wywołania.

    :param image: Nazwa obrazu (np. "myimage:latest")
    :param cmd: Lista argumentów (np. ["pip", "freeze"])
    :param entrypoint: Jeżeli podany, dodajemy --entrypoint
    :param remove: Czy dodać --rm
    :param capture_output: Czy odczytywać stdout/stderr
    :param check: Czy zgłaszać wyjątek w razie niepowodzenia
    :return: result (subprocess.CompletedProcess)
    """
    command = ["docker", "run"]
    if remove:
        command.append("--rm")
    if entrypoint:
        command.extend(["--entrypoint", entrypoint])
    command.append(image)

    if cmd:
        command.extend(cmd)

    return run_command(command, capture_output=capture_output, check=check)


def get_current_commit_sha() -> str:
    try:
        git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except Exception:
        git_sha = ""
    return git_sha


def docker_inspect(image_name: str) -> dict:
    try:
        r = run_command(
            ["docker", "inspect", image_name, "--format={{json .}}"],
            capture_output=True,
        )
        return json.loads(r.stdout.strip())
    except Exception:
        return None


def get_docker_image_digest(image_name: str) -> Optional[str]:
    image_info = docker_inspect(image_name)
    repo_digests = image_info.get("RepoDigests", [])
    if not repo_digests:
        raise None
    return repo_digests[0].split("@")[1]


def side_by_side_diff(a, b, context=3):
    """
    Porównuje listy łańcuchów `a` i `b` w układzie "side by side",
    wyświetlając różnice z uwzględnieniem zadanego kontekstu (domyślnie 3 linie).
    Linie w kontekście są grupowane, jeśli znajdują się blisko siebie.

    :param a: lista linii (np. plik tekstowy po splitlines())
    :param b: lista linii (np. plik tekstowy po splitlines())
    :param context: liczba linii kontekstu z każdej strony różnicy
    :return: lista łańcuchów znaków z porównaniem
    """
    if a == b:
        return []
    cruncher = difflib.SequenceMatcher(a=a, b=b)

    # Jeśli którakolwiek z list jest pusta, unikamy błędów przy `max`
    a_max_length = max((len(item) for item in a), default=0)
    b_max_length = max((len(item) for item in b), default=0)

    diff_lines = []

    # get_grouped_opcodes(n=context) zwraca listę „grup”.
    # Każda grupa to lista krotek (tag, alo, ahi, blo, bhi),
    # uzupełniona kontekstem n linii, jeżeli występują w pobliżu.
    grouped_opcodes = cruncher.get_grouped_opcodes(n=context)

    # Zmienna do śledzenia, czy przed aktualną grupą była przerwa
    # (czyli czy musimy wstawić np. "..." aby zaznaczyć pominięte fragmenty)
    last_ahi = 0
    last_bhi = 0

    for group in grouped_opcodes:
        # Sprawdź, czy istnieje przerwa (duży odstęp) między poprzednią a obecną grupą
        # – jeśli tak, wstawiamy np. '...' dla czytelności.
        # group[0] to pierwszy opcode w tej grupie: (tag, alo, ahi, blo, bhi)
        first_alo = group[0][1]
        first_blo = group[0][3]

        if first_alo > last_ahi or first_blo > last_bhi:
            diff_lines.append('...')

        for tag, alo, ahi, blo, bhi in group:
            if tag == 'replace':
                # Różne linie w a i b
                for left, right in itertools.zip_longest(a[alo:ahi], b[blo:bhi], fillvalue=''):
                    line = f"{left}{' ' * (a_max_length - len(left))}| {right}{' ' * (b_max_length - len(right))}"
                    diff_lines.append(line)
            elif tag == 'delete':
                # Linie usunięte z a
                for left in a[alo:ahi]:
                    line = f"{left}{' ' * (a_max_length - len(left))}< "
                    diff_lines.append(line)
            elif tag == 'insert':
                # Linie dodane w b
                for right in b[blo:bhi]:
                    line = f"{' ' * a_max_length}> {right}"
                    diff_lines.append(line)
            elif tag == 'equal':
                # Linie takie same w a i b (kontekst)
                for left_right in a[alo:ahi]:
                    line = (
                        f"{left_right}"
                        f"{' ' * (a_max_length - len(left_right))}  "
                        f"{left_right}"
                        f"{' ' * (b_max_length - len(left_right))}"
                    )
                    diff_lines.append(line)
            else:
                raise ValueError(f"Nieobsługiwany typ opcodu: {tag!r}")

        # Zaktualizuj granicę, do której doszliśmy w a i b
        # (ostatni opcode w grupie)
        last_ahi = max(last_ahi, group[-1][2])
        last_bhi = max(last_bhi, group[-1][4])

    if last_ahi < len(a) or last_bhi < len(b):
        diff_lines.append('...')

    return diff_lines


###############################################################################
# Main script
###############################################################################


def read_django_version_prod(constraints_file) -> str:
    content = Path(constraints_file).read_text()
    django_version = next(
        iter(line.strip().split("==")[1] for line in content.splitlines() if line.lower().startswith("django==")), None
    )
    if django_version is None:
        raise Exception(f"Django version not found in {constraints_file}")
    return django_version


def compute_base_variables():
    github_repository = os.environ.get("GITHUB_REPOSITORY", DEFAULT_GITHUB_REPOSITORY)
    github_organization = os.environ.get("GITHUB_ORGANIZATION", DEFAULT_GITHUB_ORGANIZATION)

    container_registry = os.environ.get("CONTAINER_REGISTRY", f"ghcr.io/{github_repository}").lower()

    django_version_prod = read_django_version_prod(repo_root / "dependencies/constraints-production.txt")
    python_version_prod = Path(repo_root / ".python-version").read_text().strip()
    django_version = os.environ.get("DJANGO_VERSION", django_version_prod)
    python_version = os.environ.get("PYTHON_VERSION", "current")
    if python_version == "current":
        python_version = python_version_prod
    image_tag = os.environ.get("IMAGE_TAG", "latest")
    variables = {
        "GITHUB_REPOSITORY": github_repository,
        "GITHUB_ORGANIZATION": github_organization,
        "CONTAINER_REGISTRY": container_registry,
        "DJANGO_VERSION_PROD": django_version_prod,
        "DJANGO_VERSION": django_version,
        "PYTHON_VERSION": python_version,
        "IMAGE_TAG": image_tag,
    }
    return variables


def before_build(image_type, env):
    config = IMAGE_CONFIG[image_type]
    image_name = config["image_name_format"].format(**env)

    if config["pull_latest_before_build"]:
        try:
            run_command(["docker", "pull", f"{image_name}:latest"], check=True)
        except subprocess.CalledProcessError:
            logger.warning("Pulling %s:latest nie powiodło się. Kontynuuję...", image_name)

    # PROD: docker pull python:<PYTHON_VERSION>-slim-bookworm
    if image_type == "prod":
        base_python = f"python:{env['PYTHON_VERSION']}-slim-bookworm"
        try:
            run_command(["docker", "pull", base_python], check=True)
        except subprocess.CalledProcessError:
            logger.warning("Pulling base python image %s nie powiodło się.", base_python)


def build_image(image_type, env, prepare_buildx_cache=False):
    config = IMAGE_CONFIG[image_type]
    image_name = config["image_name_format"].format(**env)
    image_tag = env["IMAGE_TAG"]
    dockerfile = config["dockerfile"]

    before_build(image_type, env)
    build_command = [
        "docker",
        "buildx",
        "build",
        str(repo_root),
        f"--file={dockerfile}",
        f"--tag={image_name}:{image_tag}",
        "--pull",
        f"--cache-from={image_name}:cache",
    ]

    # We need to use custom builders as we want to use cache from registry
    # and save cache to registry.
    # The default docker driver supports the inline, local, registry, and gha cache backends,
    # but only if you have enabled the containerd image store and we cann't guarantee that.
    # See: https://docs.docker.com/build/cache/backends/
    build_command += [
        "--load",
        "--builder",
        "pola_cache",
    ]

    try:
        run_command(["docker", "buildx", "inspect", "pola_cache"], check=True)
    except subprocess.CalledProcessError:
        run_command(["docker", "buildx", "create", "--name=pola_cache", "--driver=docker-container"], check=True)

    if prepare_buildx_cache:
        build_command += [f"--cache-to=type=registry,ref={image_name}:cache,mode=max"]

    if image_type == "prod":
        # Dodajemy informacje o SHA commita
        git_sha = get_current_commit_sha()
        build_command += [
            "--build-arg",
            f"RELEASE_SHA={git_sha}",
            "--label",
            f"org.opencontainers.image.revision={git_sha}",
        ]

        # Dodajemy informacje o bazowym obrazie Pythona
        base_img = f"python:{env['PYTHON_VERSION']}-slim-bookworm"
        base_img_digest = get_docker_image_digest(base_img)
        base_python_arg = f"{base_img}@{base_img_digest}" if base_img_digest else base_img
        build_command += [
            "--build-arg",
            f"BASE_PYTHON_IMAGE={base_python_arg}",
        ]

        # Dodajemy opis obrazu
        image_description = "Pola pomoze Ci odnaleźć polskie wyroby."
        build_command += [
            "--label",
            f"org.opencontainers.image.created={datetime.utcnow().isoformat()}Z",
            "--label",
            f"org.opencontainers.image.description={image_description}",
        ]
    elif image_type == "ci":
        build_command += [
            "--build-arg",
            f"PYTHON_VERSION={env['PYTHON_VERSION']}",
            "--build-arg",
            f"DJANGO_VERSION={env['DJANGO_VERSION']}",
        ]

    run_command(build_command)
    logger.info("Obraz zbudowany pomyślnie.")

    # Tag lokalny
    run_command(["docker", "tag", f"{image_name}:{image_tag}", config["local_image_name"]])

    repo_tags = docker_inspect(f"{image_name}:{image_tag}")["RepoTags"]
    logger.info("Dostępne tagi: ")
    for full_image_name in repo_tags:
        logger.info("  %s", full_image_name)


def verify_image(image_type, env):
    config = IMAGE_CONFIG[image_type]
    image_name = config["image_name_format"].format(**env)
    image_tag = env["IMAGE_TAG"]

    logger.info("Verifying %s image: %s:%s", image_type, image_name, image_tag)

    docker_run(f"{image_name}:{image_tag}", ["pip", "freeze"], remove=True, capture_output=False)

    result = docker_run(
        f"{image_name}:{image_tag}", ["-c", "pip freeze"], entrypoint="/bin/bash", remove=True, capture_output=True
    )
    container_deps = result.stdout.strip().split("\n") if result.stdout else []

    local_deps = Path(config["constraints_file"]).read_text().strip().split("\n")

    difference_found = compare_requirements(local_deps, container_deps, config["ignore_django"])
    if difference_found:
        logger.info("Wykryto różnice w zależnościach.")
        sys.exit(1)
    else:
        logger.info("Pliki constracints są prawidłowe.")

    if image_type == "prod":
        logger.info("Sprawdzam wartswy obrazu.")
        run_command(
            [
                "docker",
                "run",
                "--rm",
                "-v",
                "/var/run/docker.sock:/var/run/docker.sock",
                "ghcr.io/joschi/dive:latest",
                f"docker://{image_name}:{image_tag}",
                "--ci",
                "--lowestEfficiency",
                "0.90",
                "--highestUserWastedPercent",
                "0.25",
            ]
        )


def compare_requirements(local_deps: list, container_deps: list, ignore_django: bool) -> bool:
    """
    Porównuje listy zależności (posortowane łańcuchy) i wyświetla
    tzw. unified diff z biblioteki standardowej `difflib`.

    Zwraca True, jeśli wystąpiły jakiekolwiek różnice.
    """
    if ignore_django:
        local_deps = [dep for dep in local_deps if not dep.lower().startswith("django==")]
        container_deps = [dep for dep in container_deps if not dep.lower().startswith("django==")]

    diff_result = list(
        side_by_side_diff(
            sorted(local_deps, key=str.lower),
            sorted(container_deps, key=str.lower),
        )
    )

    if diff_result:
        logger.warning(" Różnice w zależnościach (side-by-side diff) ".center(80, "="))
        for line in diff_result:
            logger.warning(line)
        logger.warning("".center(80, "="))
        return True
    else:
        logger.info("Brak różnic w zależnościach.")
        return False


def push_image(image_type, env):
    config = IMAGE_CONFIG[image_type]
    image_name = config["image_name_format"].format(**env)
    image_tag = env["IMAGE_TAG"]

    logger.info("Pushing image: %s:%s", image_name, image_tag)

    run_command(["docker", "push", f"{image_name}:{image_tag}"])

    if image_type == "prod":
        # Tag as latest i push
        run_command(["docker", "tag", f"{image_name}:{image_tag}", f"{image_name}:latest"])
        run_command(["docker", "push", f"{image_name}:latest"])


def pull_image(image_type, env):
    if image_type != "prod":
        logger.warning("Pull jest tylko dla prod w oryginalnym skrypcie.")
        sys.exit(1)

    config = IMAGE_CONFIG[image_type]
    image_name = config["image_name_format"].format(**env)
    image_tag = env["IMAGE_TAG"]

    logger.info("Pulling image: %s:%s", image_name, image_tag)
    run_command(["docker", "pull", f"{image_name}:{image_tag}"])
    run_command(["docker", "tag", f"{image_name}:{image_tag}", f"{image_name}:latest"])
    run_command(["docker", "tag", f"{image_name}:{image_tag}", config["local_image_name"]])


def update_constraints(image_type, env):
    config = IMAGE_CONFIG[image_type]
    image_name = config["image_name_format"].format(**env)
    image_tag = env["IMAGE_TAG"]

    logger.info("Updating constraints for %s.", image_type)

    result = docker_run(
        f"{image_name}:{image_tag}", ["-c", "pip freeze"], entrypoint="/bin/bash", remove=True, capture_output=True
    )

    deps = result.stdout.strip().split("\n") if result.stdout else []
    if config["ignore_django"]:
        deps = [dep for dep in deps if not dep.lower().startswith("django==")]  # remove django

    deps_sorted = sorted(deps, key=str.lower)

    Path(config["constraints_file"]).write_text("\n".join(deps_sorted) + "\n")

    logger.info("Updated constraints in file: %s", config['constraints_file'])


def get_parser():
    parser = argparse.ArgumentParser(description="Skrypt obsługujący build, verify, push, pull, update_constraints.")

    subparsers = parser.add_subparsers(dest="action", required=True, help="Dostępne polecenia.")
    image_variants = ["ci", "bi", "prod"]

    build_parser = subparsers.add_parser("build", help="Buduje obraz.")
    build_parser.add_argument("--image-type", choices=image_variants, help="Rodzaj obrazu.")
    build_parser.add_argument(
        "--prepare-buildx-cache",
        dest='prepare_buildx_cache',
        default=False,
        action='store_true',
        help="Czy użyć buildx cache.",
    )
    build_parser.add_argument("--image-tag", default=None, help="Tag obrazu.")

    verify_parser = subparsers.add_parser("verify", help="Weryfikuje obraz.")
    verify_parser.add_argument("--image-type", choices=image_variants, help="Rodzaj obrazu.")
    verify_parser.add_argument("--image-tag", default=None, help="Tag obrazu.")

    push_parser = subparsers.add_parser("push", help="Push obrazu.")
    push_parser.add_argument("--image-type", choices=image_variants, help="Rodzaj obrazu.")
    push_parser.add_argument("--image-tag", default=None, help="Tag obrazu.")

    pull_parser = subparsers.add_parser("pull", help="Pull obrazu (tylko prod).")
    pull_parser.add_argument("--image-type", choices=['prod'], help="Rodzaj obrazu.")
    pull_parser.add_argument("--image-tag", default=None, help="Tag obrazu.")

    update_parser = subparsers.add_parser("update_constraints", help="Aktualizacja constraints.")
    update_parser.add_argument("--image-type", choices=image_variants, help="Rodzaj obrazu.")
    update_parser.add_argument("--image-tag", default=None, help="Tag obrazu.")

    return parser


def main():
    args = get_parser().parse_args()

    if args.image_tag:
        os.environ["IMAGE_TAG"] = args.image_tag

    env = compute_base_variables()

    if args.action == "build":
        prepare_cache = args.prepare_buildx_cache
        build_image(args.image_type, env, prepare_cache)
    elif args.action == "verify":
        verify_image(args.image_type, env)
    elif args.action == "push":
        push_image(args.image_type, env)
    elif args.action == "pull":
        pull_image(args.image_type, env)
    elif args.action == "update_constraints":
        update_constraints(args.image_type, env)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        logger.error("Wystąpił błąd podczas wykonywania polecenia: %s", e)
        sys.exit(e.returncode)
    except Exception as ex:
        logger.exception("Niezdefiniowany błąd: %s", ex)
        sys.exit(1)
