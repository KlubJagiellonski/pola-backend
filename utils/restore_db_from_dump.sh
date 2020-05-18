#!/bin/sh

DUMP=$1

OPS_DB_HOST="postgres://postgres:postgres@$POSTGRES_PORT_5432_TCP_ADDR:$POSTGRES_PORT_5432_TCP_PORT"
POLA_DB_HOST="postgres://postgres:postgres@$POSTGRES_PORT_5432_TCP_ADDR:$POSTGRES_PORT_5432_TCP_PORT/pola"

echo "Dropping db..."
psql "$OPS_DB_HOST" -c "DROP DATABASE pola;"

echo "Creating empty db..."
psql "$OPS_DB_HOST" -c "CREATE DATABASE pola;"

echo "Restoring db dump..."
pg_restore --verbose --clean --no-acl --no-owner -d "$POLA_DB_HOST" "$DUMP"

echo "Dump $DUMP restoration completed"
