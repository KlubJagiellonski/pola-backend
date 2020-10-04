#!/usr/bin/env bash

COMMAND="${1}"
set -euo pipefail

EXIT_CODE=0

echo "RELEASE_SHA=${RELEASE_SHA:-}"

function check_service {
    INTEGRATION_NAME=$1
    CALL=$2
    MAX_CHECK=${3:=20}

    echo -n "${INTEGRATION_NAME}: "
    while true
    do
        set +e
        LAST_CHECK_RESULT=$(eval "${CALL}" 2>&1)
        RES=$?
        set -e
        if [[ ${RES} == 0 ]]; then
            echo -e "OK."
            break
        else
            echo -n "."
            MAX_CHECK=$((MAX_CHECK-1))
        fi
        if [[ ${MAX_CHECK} == 0 ]]; then
            echo -e "ERROR!"
            echo "Maximum number of retries while checking service. Exiting"
            break
        else
            sleep 1
        fi
    done
    if [[ ${RES} != 0 ]]; then
        echo "Service could not be started!"
        echo
        echo "$ ${CALL}"
        echo "${LAST_CHECK_RESULT}"
        echo
        EXIT_CODE=${RES}
    fi
}

function verify_db_connection {
    DB_URL="${1}"

    local DETECTED_DB_BACKEND=""
    local DETECTED_DB_HOST=""
    local DETECTED_DB_PORT=""

    # Auto-detect DB parameters
    [[ ${DB_URL} =~ ([^:]*)://([^@/]*)@?([^/:]*):?([0-9]*)/([^\?]*)\??(.*) ]] && \
        DETECTED_DB_BACKEND=${BASH_REMATCH[1]} &&
        # Not used USER match
        DETECTED_DB_HOST=${BASH_REMATCH[3]} &&
        DETECTED_DB_PORT=${BASH_REMATCH[4]} &&
        # Not used SCHEMA match
        # Not used PARAMS match

    echo "DETECTED_DB_BACKEND=${DETECTED_DB_BACKEND}"

    if [[ "${DETECTED_DB_BACKEND}" != "postgres" ]]; then
      echo "Unsupported backend."
      exit 1
    fi

    [[ -z "${DETECTED_DB_PORT=}" ]] && DETECTED_DB_PORT=5432

    echo DETECTED_DB_PORT="${DETECTED_DB_PORT}"

    check_service "postgres" "nc -zvv ${DETECTED_DB_HOST} ${DETECTED_DB_PORT}" "20"
}

if [[ -n "${DATABASE_URL=}" ]]; then
  echo "Verifying db connection."
  verify_db_connection "${DATABASE_URL}"

  if [[ ${EXIT_CODE} != 0 ]]; then
      echo
      echo "Error: some of the environment failed to initialize!"
      echo
      exit 1
  fi
fi

if ! whoami &> /dev/null || [[ "$(whoami)" != "pola-backend" ]] ; then
  if [[ -w /etc/passwd ]]; then
    echo "${USER_NAME:-default}:x:$(id -u):0:${USER_NAME:-default} user:${APP_USER_HOME_DIR}:/sbin/nologin" \
        >> /etc/passwd
  fi
  export HOME="${APP_USER_HOME_DIR}"
fi

if [[ -n "${HEROKU_EXEC_URL=}" ]]; then
  bash /app/.profile.d/heroku-exec.sh
fi

if command -v "${COMMAND}"; then
  echo "Running: ${*}"
  exec "${@}"
fi

# HACK: For unknown reasons we have an extra worker running this command,
# but ... it can't be disabled because it is not visible in the Web UI.
if [[ "$#" -gt 1 ]] && [[ "$1" == "newrelic-admin" ]]; then
    while true; do echo "Sleep 60s"; sleep 60; done;
    exit 1
fi

echo "Invalid command: ${*}"
exit 1
