from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from boto3.dynamodb.conditions import Key, Attr
from tools.auth import *
from tools.docDB import *
from tools.dynamo import *
import boto3
import os
import datetime
import urllib.request
import json

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

dynamo_client = boto3.client('dynamodb', region_name="us-east-1")
s3_client = boto3.client('s3', region_name="us-east-1")

def valid_login(username, password):
    result = login({
        "username": username,
        "password": password
    })

    if result['success']:
        login_success(result['data'])
        return True
    else:
        flash(result['message'], 'login')
        return False

def login_success(data):
    session['token'] = data

def register_success():
    return redirect(url_for('login.show_login'))

def register_user(email, username, password):
    result = signup({
        "email": email,
        "username": username,
        "password": password
    })

    flash(result['message'], 'login')
    return result['success']

def logout_helper():
    if session.get('token') != None:
        session.clear()

def query_user():
    response = get_user(session.get('token')['access_token'])
    if response['success'] == False:
        flash(response['message'], 'error')
    return response['data']

def get_liked_questions():
    q_ids = []
    for question in dynamo_liked_questions(query_user()):
        q_ids.append(question['questionID'])
    return query_doc_ids(q_ids)
