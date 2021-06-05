from flask import Blueprint, flash, jsonify
from tools.decorators import login_required, logout_required
from tools.helpers import *
import json

login = Blueprint('login', __name__, template_folder='templates')
@login.route('/login', methods=['POST', 'GET'])
@logout_required
def show_login():
    error = None
    hideHeader = True
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if valid_login(email, password):
            return login_success(email)
        else:
            flash('The user email or password is incorrect')
    return render_template('login.html', hideHeader = True)

home = Blueprint('home', __name__, template_folder='templates')
@login.route('/home', methods=['GET'])
def show_home():
    error = None
    return render_template('home.html')

logout = Blueprint('logout', __name__, template_folder='templates')
@logout.route('/logout')
def show_logout():
    if session.get('user') != None:
        session.pop('user')
    return redirect(url_for('login.show_login'))

register = Blueprint('register', __name__, template_folder='templates')
@register.route('/register')
@logout_required
def show_register():
    return render_template('register.html', hideHeader = True)

register_process = Blueprint('register_process', __name__, template_folder='templates')
@register_process.route('/register_process', methods=['POST', 'GET'])
@logout_required
def show_register_process():
    if request.method =='POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if valid_register(email, username):
            register_user(email, username, password)
            return login_success(email)
        else:
            return redirect(url_for('register.show_register'))

user = Blueprint('user', __name__, template_folder='templates')
@user.route('/user', methods=['POST', 'GET'])
@login_required
def show_user():
    user = query_user(session.get('user'))
    songs = []
    searchsongs = []
    header = 'Your subscriptions'
    if request.method == 'POST':
        header = 'Results for search'
        searchsongs = scan_songs(request.form['title'], request.form['artist'], request.form['year'])
        if len(searchsongs) == 0:
            flash('No result is retrieved. Please query again')
    else:
        subs = query_user_subscriptions(session.get('user'))
        for sub in subs:
            song = query_song(sub['title'])
            songs.append(song)
    return render_template('user.html', user=user, songs=songs, searchsongs=searchsongs, header=header)

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
