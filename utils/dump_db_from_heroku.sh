#!/bin/sh

#dumps pola-app db from heroku

DUMP=$(heroku pg:backups --app pola-app | grep '^[a|b]' | head -1 | cut -f1 -d' ')
FILENAME=$(heroku pg:backups --app pola-app | grep '^[a|b]' | head -1 | cut -f3,4 -d' ')
FILENAME=$(echo "$FILENAME" | sed 's/:/_/g' | sed 's/ /_/g')
FILENAME="pola_db_${FILENAME}.dump"

curl -o "$FILENAME" "$(heroku pg:backups public-url "$DUMP" --app pola-app)"
