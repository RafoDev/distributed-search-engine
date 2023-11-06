#!/bin/bash

chmod +x corpus/start.sh inverted-index/start.sh page-rank/start.sh

cd corpus
./start.sh
cd ../inverted-index
./start.sh
cd ../page-rank
./start.sh
cd ..
