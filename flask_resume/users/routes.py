#################
#### imports ####
#################

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user, login_user

from . import users_blueprint
from .views import LoginForm, SignupForm
from flask_resume import db
from flask_resume.models import User

################
#### routes ####
################
@users_blueprint.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data
        target = User.query.filter_by(username = username).first()
        if target and target.verify_password(password):
            login_user(target, remember=remember)
            return redirect(request.args.get('next') or url_for('recipes.index'))
        else:
            flash("Incorrect username/password")
            return render_template('login.html', form=form)
    return render_template('users/login.html', form=form)

@users_blueprint.route('/signup', methods=('GET', 'POST'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        target = User.query.filter_by(username = username).first()
        if target:
            flash("Username existed")
            return render_template('users/signup.html', form=form)
        else:
            newuser = User(username = username, password = password)
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for('users.login'))
    return render_template('users/signup.html', form=form)

@users_blueprint.route('/logout', methods=('GET',))
@login_required
def logout():
    logout_user()
    return redirect(url_for('recipes.index'))