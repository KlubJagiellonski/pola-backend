#!/bin/sh

CODE=$1

curl http://localhost:8000/api/product/"$CODE"/?device_id=test

