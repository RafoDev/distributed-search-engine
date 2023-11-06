#!/bin/bash

# compatibility with aws 2
#pip install "urllib3<2.0"

chmod +x clean.py prepare-dirs.py corpus-generator.py graph-generator.py

# dirs creation for corpus and related data
python clean.py
python prepare-dirs.py

# script to get pids and download files 
python corpus-generator.py

# script to generate the pagerank graph
python graph-generator.py 
