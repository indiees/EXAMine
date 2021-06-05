import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

from tools.pages import createmusictable, populatemusictable
from tools.pages import login, home, logout, register, register_process, user
from tools.decorators import login_required

app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(home)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(register_process)
app.register_blueprint(user)
app.secret_key = "supersecretkey"

@app.route('/')
@login_required
def root():
    return redirect(url_for('login.show_login'))

@app.route('/home')
@login_required
def home():
    return redirect(url_for('home.show_home'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
