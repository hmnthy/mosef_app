#!/bin/bash

(cd ../ ; bash install.sh >> log/install.log) &&
(cd . ; bash launch.sh >> ../log/data_pipeline.log) &&
(cd ../webapp/bin; bash launch.sh >> ../../log/webapp.log )