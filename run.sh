#!/bin/bash

set -e

if netstat -an | grep -q "3307.*LISTEN" ; then
  all_ready_running=true
else
  ssh -M -S ~/my-ctrl-socket -fnNT -L 0.0.0.0:3307:localhost:3306 -i /Users/keir/.ssh/spot-key.pem ec2-user@$AS_DB_HOST
fi

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
    doorduty.local "$@"

if [ -z all_ready_running ] ; then 
  ssh -S ~/my-ctrl-socket -O exit -i /Users/keir/.ssh/spot-key.pem ec2-user@$AS_DB_HOST
fi
