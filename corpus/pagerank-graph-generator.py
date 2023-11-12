#!/usr/bin/env python3

from utils import *

if __name__ == "__main__":
    pagerank_filename = "page-rank/pagerank.txt"
    graph = json_to_graph("json/final_graph.json")
    print(graph.number_of_nodes())
    lines = ""
    for edge in graph.edges():
        lines += edge[0] + "\t" + edge[1] + "\n"
    
    s3_client.put_object(Bucket=bucket_name, Key=pagerank_filename, Body=lines)