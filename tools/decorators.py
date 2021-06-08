from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for
from tools.auth import *
from tools.helpers import *

def login_required(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
        if session.get('token') == None:
            return redirect(url_for('login.show_login'))
        if get_user(session.get('token')['access_token'])['success'] != True:
            flash('Your session has expired. please log in again.', 'login')
            return redirect(url_for('login.show_login'))
        return f(*args, **kwargs)
    return login_decorator

def logout_required(f):
    @wraps(f)
    def logout_decorator(*args, **kwargs):
        logout_helper()
        return f(*args, **kwargs)
    return logout_decorator
