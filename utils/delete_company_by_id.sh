#!/bin/sh

POLA_DB_HOST="postgres://postgres:postgres@$POSTGRES_PORT_5432_TCP_ADDR:$POSTGRES_PORT_5432_TCP_PORT/pola"

echo "Deleting queries"
psql "$POLA_DB_HOST" -c "delete from pola_query where product_id in (select id from product_product where company_id=$1)"

echo "Deleting reports"
psql "$POLA_DB_HOST" -c "delete from report_report where product_id in (select id from product_product where company_id=$1)"

echo "Deleting products"
psql "$POLA_DB_HOST" -c "delete from product_product where company_id=$1"

echo "Deleting company"
psql "$POLA_DB_HOST" -c "delete from company_company where id=$1"

echo "Company deleted "
