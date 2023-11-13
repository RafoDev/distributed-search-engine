#!/usr/bin/env python3

import requests
import networkx as nx
import matplotlib.pyplot as plt
import json
import boto3
from config import *
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
import re

s3_client = boto3.client('s3')

def preproccess(data):
    stemmer  = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    lines = data.split('\n')
    prepro_data = []

    for line in lines:
        
        line = line.lower()
        line = re.sub(r'\W+', ' ', line)
        words = word_tokenize(line)

        prepro_words = [stemmer.stem(word) for word in words if word not in stop_words]
        prepro_data.append(' '.join(prepro_words))

    return '\n'.join(prepro_data)

def graph_to_json(graph, filename):
    data = nx.json_graph.node_link_data(graph)
    file_content = json.dumps(data)
    s3_client.put_object(Bucket=bucket_name, Key=filename +
                         '.json', Body=file_content)

def json_to_graph(filename):
    result = s3_client.get_object(Bucket=bucket_name, Key=filename)
    data = json.loads(result["Body"].read().decode())
    graph = nx.json_graph.node_link_graph(data)
    return graph
