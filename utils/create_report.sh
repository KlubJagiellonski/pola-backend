#!/bin/sh

curl "https://pola-staging.herokuapp.com/a/v2/create_report?device_id=kuba-test" -H "Accept: application/json" -H "Content-type: application/json" --data '{
   "description": "Krzesło małe",
   "files_count": 4,
   "mime_type": "image/png",
   "file_ext":"png"
}'

curl "http://localhost:8000/a/update_report?device_id=kuba-test&report_id=15" -H "Accept: application/json" -H "Content-type: application/json" --data '{
   "description": "Krzesło małe 2"
}'

curl "https://pola-staging.herokuapp.com/a/v2/attach_file?device_id=kuba-test&report_id=6745" -H "Accept: application/json" -H "Content-type: application/json" --data '{
   "mime_type": "image/png",
   "file_ext":"png"
}'

curl -v -H "x-amz-acl: public-read" -H "Content-Type: image/png" "https://pola-app.s3.amazonaws.com/2aa854ae-8c98-11e5-adb5-0242ac110002.png?AWSAccessKeyId=AKIAJ5PTX4GFT7D7HVNQ&Expires=1447788488&Signature=kBkTcunllS1Ubxp0l19fRVU33cQ%3D" --upload-file aa.txt

curl -v -F file=@LICENSE "http://localhost:8000/a/attach_file?report_id=15&device_id=kuba-test"
