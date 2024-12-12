#!/bin/bash

dt=$(date +%Y)
FILE=../archived/raw/raw_data_$dt.csv

if test -f "$FILE"; then
    echo "$FILE exists. Launching integration"
else 
    echo "Downloading data"
    cd ../data_collector/bin
    bash get_data.sh
    echo "Data downloaded"
    cd ..
fi

echo "Integrating data"
cd ../data_integrator/bin
bash workflow.sh
echo "Data integrated"

echo "Processing data"
cd ../../data_processor/bin
bash workflow.sh
echo "Processing data succeeded"

cd ../bin
