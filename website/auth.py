from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = str(request.form.get('password'))
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        username = User.query.filter_by(name=name).first()
        if user:
            flash('Email already exists', category='error')
        elif username:
            flash('Username already exists', category='error')
        elif(len(email) < 3):
            flash('Email must be atleast 7 chars long', category='error')
        elif(len(name) < 3):
            flash('Name must be atleast 3 chars long', category='error')
        elif(len(password1) < 4):
            flash('Password must be atleast 5 chars long', category='error')
        elif(password1!=password2):
            flash('Passwords dont match :(', category='error')
        else:
            new_user = User(email=email, name=name.capitalize(), password=generate_password_hash(password1, method='sha256'), bufferattempt=0)
            db.session.add(new_user)
            db.session.commit()
            current_id = new_user.id
            stat = Stats(level=0, author=current_id, sumoftimes=0, sumofattempts=0, times="", attempts="")
            db.session.add(stat)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('User account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user = current_user)
