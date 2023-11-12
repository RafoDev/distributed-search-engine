#!/usr/bin/env python3

from utils import *

if __name__ == "__main__":
    graph = json_to_graph("json/final_graph.json")
    print(graph.number_of_nodes())
    lines = ""
    for edge in graph.edges():
        lines += edge[0] + "\t" + edge[1] + "\n"
    print(lines)