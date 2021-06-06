from flask import Blueprint, render_template
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