from flask import Blueprint, render_template, redirect, url_for, flash, session
from app import db, bcrypt
from app.models import User
from app.auth.forms import SignupForm, LoginForm

auth = Blueprint('auth', __name__)

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('auth.signup'))
        
        # Hash password and create user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Store user info in session
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('todos.dashboard'))
        else:
            flash('Login failed. Please check username and password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    if is_logged_in():
        session.pop('user_id', None)
        session.pop('username', None)
        flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))
