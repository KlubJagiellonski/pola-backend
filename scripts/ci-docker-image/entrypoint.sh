#!/usr/bin/env bash

COMMAND="${1}"
set -euo pipefail

EXIT_CODE=0

function check_service {
    INTEGRATION_NAME=$1
    CALL=$2
    MAX_CHECK=${3:=1}

    echo -n "${INTEGRATION_NAME}: "
    while true
    do
        set +e
        LAST_CHECK_RESULT=$(eval "${CALL}" 2>&1)
        RES=$?
        set -e
        if [[ ${RES} == 0 ]]; then
            echo -e " \e[32mOK.\e[0m"
            break
        else
            echo -n "."
            MAX_CHECK=$((MAX_CHECK-1))
        fi
        if [[ ${MAX_CHECK} == 0 ]]; then
            echo -e " \e[31mERROR!\e[0m"
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

echo "Checking environment:"
check_service "postgres" "nc -zvv postgres 5432" "20"

if [[ ${EXIT_CODE} != 0 ]]; then
    echo
    echo "Error: some of the CI environment failed to initialize!"
    echo
    exit 1
fi

if command -v "${COMMAND}"; then
  echo "Running: ${*}"
  exec "${@}"
fi

echo "Running: /app/manage.py ${*}"
exec "/app/manage.py" "${@}"
