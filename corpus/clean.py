#!/usr/bin/env python3

import boto3
from config import bucket_name

s3 = boto3.resource('s3')

bucket = s3.Bucket(bucket_name)

bucket.objects.all().delete()