import datetime
from flask import Flask, render_template, request, session, redirect, url_for
#from flask_session import Session

from tools.pages import login, home, register
application = Flask(__name__)
application.register_blueprint(login)
application.register_blueprint(home)
application.register_blueprint(register)
#application.secret_key = "supersecretkey"

@application.route('/')
def root():
    return redirect(url_for('login.show_login'))

@application.route('/home')
def home():
    return redirect(url_for('home.show_home'))

if __name__ == '__main__':
    application.run() #host='127.0.0.1', port=80, debug=True
