#!/bin/sh

function finish {
    disown
}
trap finish EXIT

set -e

export PROJECT_ROOT=$(pwd)
export SERVER_LOG=$PROJECT_ROOT/var/log/StanfordCoreNLPServer.$(date +%s).log
INPUT_XML_FILENAME=$1
OUTPUT_DIR=$2

mkdir -p var/log
mkdir -p var/tmp

rm -rf venv
virtualenv -p /bin/python3.4 venv
source ./venv/bin/activate

# Start the server
$PROJECT_ROOT/src/server.sh &

# Wait for it to start, then get active port number
sleep 5 # TODO this is not a good way to wait for the server to start

# Get the active port number
PORT=$(grep "listening at .*:\([0-9]\+\)$" ${SERVER_LOG} | sed "s/.*[:.]//g")
echo "CoreNLP Port: ${PORT}"

pip install -r ${PROJECT_ROOT}/src/requirements.txt

set +e
python ${PROJECT_ROOT}/src/main.py $INPUT_XML_FILENAME $OUTPUT_DIR $PORT

deactivate
