#!/bin/sh

curl http://localhost:8000/api/create_report?device_id=kuba-test -H "Accept: application/json" -H "Content-type: application/json" --data '{
   "description": "Krzesło małe"
}'

curl http://localhost:8000/api/update_report?device_id=kuba-test -H "Accept: application/json" -H "Content-type: application/json" --data '{
   "report_id": 8,
   "description": "Krzesło małe 2"
}'
