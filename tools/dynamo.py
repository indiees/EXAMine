from boto3.dynamodb.conditions import Key, Attr
from tools.helpers import *
import boto3
import json

dynamodb=boto3.resource("dynamodb", region_name="us-east-1")
table=dynamodb.Table("likes")

def dynamo_liked_questions(user):
    id = user['UserAttributes'][0]['Value']

    response=table.query(
        IndexName="userID-index",
        KeyConditionExpression=Key("userID").eq(id)
    )

    return response['Items']

def set_client_liked(questions, userID):
    for question in questions:
        response=table.query(
            IndexName="userID-index",
            KeyConditionExpression=Key("userID").eq(userID)
        )
        question["liked"]=False
        for item in response ["Items"]:
            if item["questionID"]==question["_id"]["$oid"]:
                question["liked"]=True
    return questions
