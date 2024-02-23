from flask import Blueprint, session, render_template, request, flash, redirect, url_for
import sqlite3, re

auth = Blueprint('auth', __name__)

# Login Page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Connect to the database
        conn = sqlite3.connect('userDatabase.db')
        cur = conn.cursor()
        cur.execute("SELECT id, email, userPass FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        if user is None:
                flash('User not found. Please check your email.', 'error')
        elif user[2] != password:
                flash('Incorrect password. Please try again.', 'error')
        else:
                flash('Logged in successfully!', 'success')
                conn.close()
                session['logged_in'] = True  # Set session variable to indicate user is logged in
                return redirect(url_for("auth.userPage")) # Upon successful login, redirect user to userPage
    return render_template("login.html")

#SignUp page
@auth.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')
        passwordCon = request.form.get('passwordCon')
        username = request.form.get('username')
        phoneNum = request.form.get('phoneNum')
        
        # String input validations
        if len(email) < 4:
            flash('Email must be greater than 3 characters!', category='error')
        elif len(firstName) < 2:
            flash('First Name must be greater than 1 character!', category='error')
        elif len(lastName) < 2:
            flash('Last Name must be greater than 1 character!', category='error')
        elif password != passwordCon:
            flash('Passwords don\'t match!', category='error')
        elif len(password) < 12:
            flash('Password must be at least 12 characters', category='error')
        elif not re.match(r'^\d{3}-\d{3}-\d{4}$', phoneNum):
            flash('Phone number must be in the format XXX-XXX-XXXX', category='error')
        else:
            # Connect to the database
            conn = sqlite3.connect('userDatabase.db')
            cur = conn.cursor()

            # Insert the user information into the database
            cur.execute("INSERT INTO users (firstname, lastName, email, userPass, username, phoneNum) VALUES (?, ?, ?, ?, ?, ?)", (firstName, lastName, email, password, username, phoneNum))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            flash('Account created!', category='success')
            session['logged_in'] = True  # Set session variable to indicate user is logged in
            return redirect(url_for("auth.userPage")) # Upon signing up, redirect user to userPage
    return render_template("signUp.html")

# About Page
@auth.route('/about')
def about():
    return render_template("about.html")

# user Page
@auth.route('/userPage')
def userPage():
     return render_template("userPage.html")

# Logout route
@auth.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear the session variable
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout