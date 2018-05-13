#!/bin/bash
rm -rf venv
mkdir venv
cd venv
virtualenv -p python3 python3_virtualenv
source ./python3_virtualenv/bin/activate
