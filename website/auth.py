#for authentication
from flask import Blueprint, request, redirect, url_for
from flask import flash #to show message on screen
from flask.templating import render_template
from flask_login.utils import login_required
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash #to secure password
from . import db
from flask_login import login_user, login_required, logout_user, current_user

#names of blueprints
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user =User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exists', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #you can't logged out unless you are logged in(it is a decorator)
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #if user already exists
        user =User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First Name  must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('password don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password mus be at least 7 characters', category='error')
        else:
            #columns same as in models.py
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256')) #sha256=>hashing algorithm
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account Created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


