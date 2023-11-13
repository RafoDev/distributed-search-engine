#!/usr/bin/env python3

from re import findall
from sys import stdin
from os import path, environ

import sys

for line in stdin:

        doc_id = environ["map_input_file"]

        doc_id = path.split(doc_id)[-1]
        
        words = line.rstrip('\n').split()

        for word in words:   
            print ("%s\t%s:1" % (word, doc_id))
            #print ('{0}, {1}, {2}'.format( word.lower(), doc_id, index))
    