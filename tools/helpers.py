from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from boto3.dynamodb.conditions import Key, Attr
from tools.auth import *
import boto3
import os
import datetime
import urllib.request
import json

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

dynamo_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')

def valid_login(email, password):
    user = query_user(email)
    if user:
        if password == user['password']:
            return True
    return False

def login_success(email):
    session['user'] = email
    return redirect(url_for('login.show_login'))

def valid_register(email, username):
    valid = True
    # email_exists = query_user(email)
    # username_exists = scan_user_attr(key='user_name', value=username)
    # if email_exists:
    #     flash(f'The email "{email}" already exists')
    #     valid = False
    # if username_exists:
    #     flash(f'The username "{username}" already exists')
    #     valid = False
    return valid

def register_user(email, username, password):
    result = signup({
        "email": email,
        "username": username,
        "password": password
    })

    if(result['success']):
        flash(result['message'])

def query_user(email, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('login')
    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    if len(response['Items']) == 0:
        return None
    else:
        return response['Items'][0]

def query_user_subscriptions(email, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('subscriptions')
    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    return response['Items']

def delete_subscription(title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('subscriptions')
    try:
        response = table.delete_item(
            Key={
                'email': session.get('user'),
                'title': title
            }
        )
    except ClientError as e:
        flash(e.response['Error']['Message'])
    else:
        return response

def add_subscription(title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('subscriptions')
    try:
        response = table.put_item(Item={
            'email': session.get('user'),
            'title': title
        })
    except ClientError as e:
        flash(e.response['Error']['Message'])
    else:
        return response

def query_song(title, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('music')
    response = table.query(
        KeyConditionExpression=Key('title').eq(title)
    )
    if len(response['Items']) == 0:
        return None
    else:
        return response['Items'][0]

def scan_user_attr(key, value, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('login')
    response = table.scan(
        FilterExpression=Attr(key).eq(value)
    )

    if len(response['Items']) == 0:
        return None
    else:
        return response['Items'][0]

def scan_songs(title, artist, year, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    if title == "":
        title = None
    if artist == "":
        artist = None
    if year == "":
        year = None


    table = dynamodb.Table('music')
    response = table.scan(
        FilterExpression=Attr('title').contains(title) | Attr('artist').contains(artist) | Attr('year').contains(year)
    )

    return response['Items']

def get_items():
    response = dynamo_client.scan(TableName='login')
    return response.get('Items', [])

def create_music_table():
    table = dynamo_client.create_table(
        TableName='music',
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'artist',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'  # Partition key
            },
            {
                'AttributeName': 'artist',
                'AttributeType': 'S'  # Sort key
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    flash("table created")
    return table

def populate_music_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('music')
    with open('a2.json') as json_file:
        data = json.load(json_file)
        for song in data['songs']:
            url = song['img_url']
            filename, file = urllib.request.urlretrieve (url, url.rsplit('/', 1)[1])
            s3_client.upload_file(filename, 'jackcc2021a2images', filename)
            table.put_item(Item={
                'title': song['title'],
                'artist': song['artist'],
                'year': song['year'],
                'web_url': song['web_url'],
                'image_url': 'https://jackcc2021a2images.s3.amazonaws.com/' + url.rsplit('/', 1)[1]
            })
            flash(f"succesfully added {song['title']} by {song['artist']} to table music")
