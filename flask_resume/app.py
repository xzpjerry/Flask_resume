from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf.csrf import CSRFProtect
from flask_uploads import configure_uploads, patch_request_class
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user

from werkzeug.utils import secure_filename

import os, base64

from gbconfig import db, AVATARS
from models import User, Resume, Basic_info
from views import LoginForm, SignupForm, BasicResumeEditForm

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configurate avatar photos storage location
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads')# Temp folder
configure_uploads(app, AVATARS)
patch_request_class(app)  # set maximum file size, default is 16MB)

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# db config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'# Debug purpose
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
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data
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
        username = form.username.data
        password = form.password.data
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


@app.route('/resume/edit/<string:resume_type>', methods=('POST',))
@login_required
def edit_resume(resume_type):
    resume = current_user.resume
    if resume == None:
        resume = Resume()
        current_user.resume = resume
        db.session.add(resume)
        db.session.commit()
    if resume_type == "basic_info":
        form = BasicResumeEditForm()
        if not form.validate_on_submit():
            return redirect(url_for('resume'))
        basic_info = resume.basic_info
        f = form.portrait.data
        avatar_filename = AVATARS.save(f, name=secure_filename(f.filename))
        avatar_url = AVATARS.url(avatar_filename)
        if basic_info == None:
            resume.basic_info = Basic_info(name = form.name.data, nation = form.nation.data, region = form.region.data, birth = form.birth.data, portrait_URL = avatar_url)
            db.session.add(resume.basic_info)
        else:
            basic_info.name = form.name.data
            basic_info.nation = form.nation.data
            basic_info.region = form.region.data
            basic_info.birth = form.birth.data
            basic_info.portrait_URL = avatar_url
        db.session.commit()
    return redirect(url_for('resume'))
        

@app.route('/resume', methods=('GET', ))
@login_required
def resume():
    if current_user.resume == None:
        return render_template('resume.html', basic_info_form = BasicResumeEditForm())
    return render_template('resume.html')

@app.route('/logout', methods=('GET',))
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)