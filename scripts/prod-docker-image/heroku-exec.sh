#!/usr/bin/env bash

# shellcheck disable=SC1090
[ -z "$SSH_CLIENT" ] && source <(curl --fail --retry 3 -sSL "$HEROKU_EXEC_URL")
