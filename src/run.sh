#!/bin/sh

function finish {
    disown
}
trap finish EXIT

set -e

export PROJECT_ROOT=$(pwd)
export SERVER_LOG=$PROJECT_ROOT/var/log/StanfordCoreNLPServer.$(date +%s).log

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

INPUT_XML_FILENAME="/dropbox/17-18/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml"
OUTPUT_DIR="${PROJECT_ROOT}/outputs/D3/"

set +e
python ${PROJECT_ROOT}/src/main.py $INPUT_XML_FILENAME $OUTPUT_DIR $PORT

deactivate
