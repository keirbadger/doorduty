#!/bin/bash

set -e


docker build -t doorduty.test -f Dockerfile.test .
docker run -it --rm \
    -e AS_DB_NAME=$AS_DB_NAME \
    -e AS_DB_USER=$AS_DB_USER \
    -e AS_DB_PORT=$AS_DB_PORT \
    -e AS_DB_PASS=$AS_DB_PASS \
    doorduty.test pytest "$@"

