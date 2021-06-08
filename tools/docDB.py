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
