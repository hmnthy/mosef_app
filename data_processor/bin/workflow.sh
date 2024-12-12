#!/bin/bash

dt=$(date +%Y)
STAGED_FILE=../../archived/staged/staged_data_$dt.csv

if test -f "$STAGED_FILE"; then
  echo "$STAGED_FILE exists. Launching integration"
  bash run.sh
  echo "Data processing succeeded"
  # Vérifie si le répertoire d'archive existe, sinon le créer
  if [ ! -d "../../archived/staged" ]; then
    mkdir -p ../../archived/staged
  fi
  mv $STAGED_FILE ../../archived/staged/staged_data_$dt.csv
else
  echo "No staged file detected"
fi


