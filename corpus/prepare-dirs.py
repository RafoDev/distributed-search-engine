#!/usr/bin/env python3

import boto3
from config import bucket_name

s3_client = boto3.client('s3')

s3_client.put_object(Bucket=bucket_name, Key='data/')

s3_client.put_object(Bucket=bucket_name, Key='inverted-index/')

s3_client.put_object(Bucket=bucket_name, Key='page-rank/')

s3_client.put_object(Bucket=bucket_name, Key='corpus/pdf/')
s3_client.put_object(Bucket=bucket_name, Key='corpus/txt/')