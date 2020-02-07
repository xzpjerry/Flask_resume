from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user

from os import urandom

from dbconfig import db
from models import User, Resume
from views import LoginForm, SignupForm

app = Flask(__name__)
app.secret_key = urandom(24)

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db.init_app(app)

# context refresh
app.app_context().push()
# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)

@app.route('/index', methods=('GET',))
@app.route('/', methods=('GET',))
def index(): 
    return render_template('index.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        remember = request.form.get('remember_me', False)
        target = User.query.filter_by(username = username).first()
        if target and target.verify_password(password):
            login_user(target, remember=remember)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash("Incorrect username/password")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        target = User.query.filter_by(username = username).first()
        if target:
            flash("Username existed")
            return render_template('signup.html', form=form)
        else:
            newuser = User(username = username, password = password)
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)