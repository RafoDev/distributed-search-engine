#!/bin/bash

# compatibility with aws 2
#pip install "urllib3<2.0"

chmod +x clean.py
chmod +x prepare-dirs.py.py
chmod +x corpus-generator.py
chmod +x graph-generator.py

# dirs creation for corpus and related data
python clean.py
python prepare-dirs.py

# script to get pids and download files 
python corpus-generator.py

# script to generate the pagerank graph
python graph-generator.py 
