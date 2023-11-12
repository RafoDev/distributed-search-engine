#!/usr/bin/env python3

import requests
import networkx as nx
import matplotlib.pyplot as plt
import json
import boto3
from config import *

s3_client = boto3.client('s3')

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
