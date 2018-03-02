#!/bin/bash

if command ipconfig getifaddr en0 >/dev/null 2>&1; then
  host_ip=$(ipconfig getifaddr en0)
else
  host_ip=$(hostname -i)
fi

docker build -t doorduty.local .
docker run -it --rm \
    -e AS_DB_NAME=$AS_DB_NAME \
    -e AS_DB_USER=$AS_DB_USER \
    -e AS_DB_PORT=$AS_DB_PORT \
    -e AS_DB_PASS=$AS_DB_PASS \
    --add-host localhost:$host_ip \
    doorduty.local
