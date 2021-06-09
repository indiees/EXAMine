import boto3 , uuid, requests
from tools.helpers import *
from flask import Blueprint, render_template, request, redirect, url_for, flash
from boto3.dynamodb.conditions import Key
from tools.decorators import *
from tools.docDB import *
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
    questions=requests.get("https://73l3jdpqz2.execute-api.us-east-1.amazonaws.com/queryDocs").json()
    userID=query_user()["UserAttributes"][0]["Value"]
    # popular_questions=[]
    # popular_questions_IDs=[]
    # pop={
    #     "1":0,
    #     "2":0,
    #     "3":0,
    #     "4":0,
    #     "5":0,
    # }
    # response=table.scan()
    # #calculating popularity of all items
    # for item in response ["Items"]:
    #     if item["questionID"] in pop:
    #         pop[item["questionID"]]+=1
    #     else:
    #         pop[item["questionID"]]=1
    # print(pop)
    # for i in range(0,5):
    #     max_key=max(pop, key=pop.get)
    #     popular_questions_IDs.append(
    #         {
    #             "questionID": max_key,
    #             "num_likes": pop[max_key]
    #         }
    #     )
    #     pop.pop(max_key)
    # print(popular_questions_IDs)
    # for question in popular_questions_IDs:
    #     print(question)
    #     popular_questions.append(
    #         {
    #             "questionID": question["questionID"],
    #             "num_likes": question["num_likes"],
    #             "question": "question "+ question["questionID"]  #manual for now
    #
    #         }
    #     )
    for question in questions:
        print(question)
        response=table.query(
            IndexName="userID-index",
            KeyConditionExpression=Key("userID").eq(userID)
        )
        question["liked"]=False
        for item in response ["Items"]:
            if item["questionID"]==question["_id"]["$oid"]:
                question["liked"]=True
    return render_template('home.html' ,questions=questions, userID=userID)

register = Blueprint('register', __name__, template_folder='templates')
@register.route('/register')
def show_register():
    return render_template('register.html', hideHeader = True)

question = Blueprint('question', __name__, template_folder='templates')
@question.route('/question/<questionID>', methods=['GET'])
@login_required
def show_question(questionID=1):
    print(id)
    response=table.query(
        IndexName="userID-index",
        KeyConditionExpression=Key("userID").eq("1")
    )
    liked=False
    for item in response ["Items"]:
        if item["questionID"]==questionID:
            liked=True
    question={ #setting this manually for now
        "question": "Compounds that are capable of accepting electrons, such as o 2 or f2, are called what?",
        "distractor3": "residues",
        "distractor1": "antioxidants",
        "distractor2": "Oxygen",
        "correct_answer": "oxidants",
        "support": "Oxidants and Reductants Compounds that are capable of accepting electrons, such as O 2 or F2, are calledoxidants (or oxidizing agents) because they can oxidize other compounds. In the process of accepting electrons, an oxidant is reduced. Compounds that are capable of donating electrons, such as sodium metal or cyclohexane (C6H12), are calledreductants (or reducing agents) because they can cause the reduction of another compound. In the process of donating electrons, a reductant is oxidized. These relationships are summarized in Equation 3.30: Equation 3.30 Saylor URL: http://www. saylor. org/books."
    }
    for field in question:
        question[field]=question[field][0].upper()+question[field][1:]
    return render_template('question.html', question=question, questionID=questionID, liked=liked)

@question.route("/question/<questionID>/like")
@login_required
def like_question (questionID):
    userID=query_user()["UserAttributes"][0]["Value"]
    print("liking question:" + questionID)
    response=table.put_item(
        Item={
            "questionID": str(questionID),
            "userID": userID, 
            "ID": uuid.uuid1().hex
        }
    )
    return redirect (request.args.get("origin"))

@question.route("/question/<questionID>/unlike")
@login_required
def unlike_question (questionID):
    userID=query_user()["UserAttributes"][0]["Value"]
    print("unliking question:" + questionID)

    return redirect (request.args.get("origin"))

liked_questions = Blueprint('liked_questions', __name__, template_folder='templates')
@liked_questions.route('/liked_questions', methods=['GET'])
@login_required
def show_liked_questions():
    userID=query_user()["UserAttributes"][0]["Value"]
    questions=[]
    response=table.query(
        IndexName="userID-index",
        KeyConditionExpression=Key("userID").eq(userID)
    )
    for item in response ["Items"]:
        questions.append(
            {
                "question": "question " + item ["questionID"],
                "questionID": item ["questionID"],
            }

        )
    return render_template('liked_questions.html', questions=questions);

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
