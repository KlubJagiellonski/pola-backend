#!/bin/sh

curl http://localhost:8000/api/create_report?device_id=kuba-test -H "Accept: application/json" -H "Content-type: application/json" --data '{
   "description": "Krzesło małe"
}'

curl http://localhost:8000/api/update_report?device_id=kuba-test&report_id=8 -H "Accept: application/json" -H "Content-type: application/json" --data '{
   "description": "Krzesło małe 2"
}'

curl -v -F file=@LICENSE http://localhost:8000/a/attach_file?report_id=8"&"device_id=kuba-test