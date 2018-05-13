#!/bin/bash
export PROJECT_ROOT=$(pwd)
export SERVER_LOG=$PROJECT_ROOT/var/log/StanfordCoreNLPServer.$(date +%s).log

mkdir -p var/log

rm -rf venv
mkdir venv
cd venv
virtualenv -p python3 python3_virtualenv
source ./python3_virtualenv/bin/activate

# Start the server
$PROJECT_ROOT/src/server.sh &

# Wait for it to start, then get active port number
sleep 5 # TODO this is not a good way to wait for the server to start

# Get the active port number
PORT=$(grep "listening at .*:\([0-9]\+\)$" ${SERVER_LOG} | sed "s/.*[:.]//g")
echo $PORT

pip install -r ${PROJECT_ROOT}/src/requirements.txt

INPUT_XML_FILENAME="/dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml"
OUTPUT_DIR="${PROJECT_ROOT}/output/D3/"
python ${PROJECT_ROOT}/src/main.py $INPUT_XML_FILENAME $OUTPUT_DIR $PORT

deactivate
