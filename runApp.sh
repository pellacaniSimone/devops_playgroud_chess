#!/bin/sh

cd /var/log/
#python3 -m http.server 2>&1  >> /var/log/serverLog.log &
python3 -m http.server &
P1=$! # get pid

cd /python-docker/
python3 -m flask run --host=0.0.0.0 --port=80 --with-threads --debug 2>&1  >> /var/log/flaskLog.log &
P2=$! # get pid
wait $P1 $P2 # aspetta pid
#wait $P1 # aspetta pid

