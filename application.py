import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from tools.pages import *

application = Flask(__name__)

application.secret_key = 'super secret key'
application.config['SESSION_TYPE'] = 'filesystem'

application.config.from_object(__name__)
Session(application)

application.register_blueprint(login)
application.register_blueprint(home)
application.register_blueprint(register)
application.register_blueprint(liked_questions)
application.register_blueprint(login_process)
application.register_blueprint(logout)
application.register_blueprint(register_process)

@application.route('/')
def root():
    return redirect(url_for('login.show_login'))

if __name__ == '__main__':
    application.debug = True
    application.run()
