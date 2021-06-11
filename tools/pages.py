import boto3 , uuid, requests
from tools.helpers import *
from flask import Blueprint, render_template, request, redirect, url_for, flash
from boto3.dynamodb.conditions import Key
from tools.decorators import *
from tools.docDB import *
from tools.dynamo import *
dynamodb=boto3.resource("dynamodb", region_name="us-east-1")
table=dynamodb.Table("likes")

login = Blueprint('login', __name__, template_folder='templates')
@login.route('/login', methods=['POST', 'GET'])
def show_login():
    return render_template('login.html')

login_process = Blueprint('login_process', __name__, template_folder='templates')
@login_process.route('/login_process', methods=['POST', 'GET'])
def show_login_process():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_login(username, password):
            return redirect(url_for('home.show_home'))
        else:
            return redirect(url_for('login.show_login'))

home = Blueprint('home', __name__, template_folder='templates')
@home.route('/home', methods=['GET'])
@login_required
def show_home():
    userID = query_user()["UserAttributes"][0]["Value"]
    questions = set_client_liked(query_most_liked_docs(10), userID)
    return render_template('home.html', questions=questions, userID=userID)

register = Blueprint('register', __name__, template_folder='templates')
@register.route('/register')
def show_register():
    return render_template('register.html', hideHeader = True)

liked_questions = Blueprint('liked_questions', __name__, template_folder='templates')
@liked_questions.route('/liked_questions', methods=['GET'])
@login_required
def show_liked_questions():
    user = query_user()
    userID = user["UserAttributes"][0]["Value"]
    questions = set_client_liked(get_liked_questions(), userID)
    for question in questions:
        question["liked"]=True
    return render_template('liked_questions.html', questions=questions, userID=userID, user=user)

logout = Blueprint('logout', __name__, template_folder='templates')
@logout.route('/logout')
def show_logout():
    logout_helper()
    flash('You have been logged out.', 'login')
    return redirect(url_for('login.show_login'))


register_process = Blueprint('register_process', __name__, template_folder='templates')
@register_process.route('/register_process', methods=['POST', 'GET'])
@logout_required
def show_register_process():
    if request.method =='POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if register_user(email, username, password):
            return register_success()
        else:
            return redirect(url_for('register.show_register'))
