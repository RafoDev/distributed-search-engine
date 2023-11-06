import json
import boto3
from pymongo import MongoClient
from config import bucket_name, db

s3 = boto3.resource('s3')

collection_ii = db['inverted_index']
collection_pr = db['page_rank']


def parse_line_to_document_ii(line):
    word, postings = line.split('\t', 1)
    postings_data = postings.split(',')
    postings_list = [{"file": posting.split(':')[0], "count": int(
        posting.split(':')[1])} for posting in postings_data]
    return {"word": word, "postings": postings_list}


def parse_line_to_document_pr(line):
    parts = line.split('\t')
    if len(parts) != 2:
        return None
    filename, rank = parts
    return {"filename": filename, "rank": float(rank)}


obj_ii = s3.Object(bucket_name, 'inverted-index/result/part-00000')
with obj_ii.get()['Body'] as file:
    for line in file:
        line = line.decode('utf-8')
        if line.strip():
            document = parse_line_to_document_ii(line)
            collection_ii.insert_one(document)

obj_pr = s3.Object(bucket_name, 'page-rank/result/part-00000')
with obj_pr.get()['Body'] as file:
    for line in file:
        line = line.decode('utf-8')
        document = parse_line_to_document_pr(line)
        if document:
            collection_pr.insert_one(document)
