import pymongo
import sys
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json


def query_docs(limitNo):
    client = boto3.client('lambda', region_name="us-east-1")

    resp = client.invoke(
        FunctionName="queryDocs",
        Payload=json.dumps({
            "limit": limitNo
        })
    )

    payload = json.loads(resp["Payload"].read())

    return json.loads(payload['body'])

def query_doc_id(id):
    client = boto3.client('lambda', region_name="us-east-1")

    resp = client.invoke(
        FunctionName="queryDocByID",
        Payload=json.dumps({
            "question_id": id
        })
    )

    payload = json.loads(resp["Payload"].read())

    return json.loads(payload['body'])

def query_most_liked_docs(limitNo):
    client = boto3.client('lambda', region_name="us-east-1")

    resp = client.invoke(
        FunctionName="queryMostLikedDocs",
        Payload=json.dumps({
            "limit": limitNo
        })
    )

    payload = json.loads(resp["Payload"].read())

    return json.loads(payload['body'])

def query_doc_ids(q_ids):
    client = boto3.client('lambda', region_name="us-east-1")

    resp = client.invoke(
        FunctionName="queryDocsByID",
        Payload=json.dumps({
            "question_ids": q_ids
        })
    )

    payload = json.loads(resp["Payload"].read())
    
    return json.loads(payload['body'])
