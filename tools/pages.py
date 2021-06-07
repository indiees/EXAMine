import boto3, uuid
from flask import Blueprint, render_template, request, redirect, url_for
from boto3.dynamodb.conditions import Key
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
def show_home():
    return render_template('home.html')

register = Blueprint('register', __name__, template_folder='templates')
@register.route('/register')
def show_register():
    return render_template('register.html', hideHeader = True)

question = Blueprint('question', __name__, template_folder='templates')
@question.route('/question/<questionID>', methods=['GET'])
def show_question(questionID=1):
    print(id)
    dynamodb=boto3.resource("dynamodb")
    table=dynamodb.Table("likes")
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
def like_question (questionID):
    print("liking question:" + questionID)
    dynamodb=boto3.resource("dynamodb")
    table=dynamodb.Table("likes")
    response=table.put_item(
        Item={
            "questionID": str(questionID),
            "userID": "1", #manual for now
            "ID": uuid.uuid1().hex
        }
    )
    print(response)
    return redirect(url_for('question.show_question', questionID=questionID))

@question.route("/question/<questionID>/unlike")
def unlike_question (questionID):
    print("unliking question:" + questionID)
    dynamodb=boto3.resource("dynamodb")
    table=dynamodb.Table("likes")

    response=table.query(
        IndexName="userID-index",
        KeyConditionExpression=Key("userID").eq("1") 
    )
    print(response["Items"])
    with table.batch_writer()as batch:
        for item in response["Items"]:
            if item["questionID"]==questionID:

                batch.delete_item(
                    Key={
                        "ID":item["ID"]
                    }
                )
    
    return redirect(url_for('question.show_question', questionID=questionID))

'''
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

remove_song = Blueprint('remove_song', __name__, template_folder='templates')
@remove_song.route('/remove_song', methods=['POST', 'GET'])
@login_required
def show_remove_song():
    if request.method == 'POST':
        success = delete_subscription(request.form['title'])
        if success:
            flash(f"{request.form['title']} deleted from subscriptions")
    return redirect(url_for('user.show_user'))

add_song = Blueprint('add_song', __name__, template_folder='templates')
@add_song.route('/add_song', methods=['POST', 'GET'])
@login_required
def show_add_song():
    if request.method == 'POST':
        success = add_subscription(request.form['title'])
        if success:
            flash(f"{request.form['title']} added to subscriptions")
    return redirect(url_for('user.show_user'))

createmusictable = Blueprint('createmusictable', __name__, template_folder='templates')
@createmusictable.route('/createmusictable')
def show_createmusictable():
    table = create_music_table()
    flash("Table created")
    return redirect(url_for('login.show_login'))

populatemusictable = Blueprint('populatemusictable', __name__, template_folder='templates')
@populatemusictable.route('/populatemusictable')
def show_populatemusictable():
    populate_music_table()
    return redirect(url_for('login.show_login'))
'''