from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for

def login_required(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
        #if session.get('user') == None:
            #return redirect(url_for('login.show_login'))
        return f(*args, **kwargs)
    return login_decorator

def logout_required(f):
    @wraps(f)
    def logout_decorator(*args, **kwargs):
        #if session.get('user') != None:
            #return redirect(url_for('user.show_user'))
        return f(*args, **kwargs)
    return logout_decorator
