#!/bin/bash
export PROJECT_ROOT=$(pwd)
export SERVER_LOG=$PROJECT_ROOT/var/log/StanfordCoreNLPServer.$(date +%s).log

mkdir -p var/log

#rm -rf venv
#mkdir venv
#cd venv
#virtualenv -p python3 python3_virtualenv
#source ./python3_virtualenv/bin/activate
#
#pip install pycorenlp
## TODO main script here

# Try to start the server
$PROJECT_ROOT/src/server.sh &
sleep 10
disown

cat $SERVER_LOG

deactivate
