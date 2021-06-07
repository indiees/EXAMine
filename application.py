import datetime
from flask import Flask, render_template, request, session, redirect, url_for
#from flask_session import Session

from tools.pages import login, home, register, question, liked_questions
application = Flask(__name__)
application.register_blueprint(login)
application.register_blueprint(home)
application.register_blueprint(register)
application.register_blueprint(question)
application.register_blueprint(liked_questions)
#application.secret_key = "supersecretkey"

@application.route('/')
def root():
    return redirect(url_for('login.show_login'))

if __name__ == '__main__':
    application.run() #host='127.0.0.1', port=80, debug=True
