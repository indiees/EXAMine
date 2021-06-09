from boto3.dynamodb.conditions import Key, Attr
from tools.helpers import *
import boto3
import json

dynamodb=boto3.resource("dynamodb", region_name="us-east-1")
table=dynamodb.Table("likes")

def dynamo_liked_questions(user):
    id = user['UserAttributes'][2]['Value']

    response=table.query(
        IndexName="userID-index",
        KeyConditionExpression=Key("userID").eq(id)
    )

    return response['Items']
