from flask import Blueprint, render_template, request, flash
import sqlite3, re

auth = Blueprint('auth', __name__)

equations = [] # Creating equation array
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
                render_template("home.html")
        conn.close()
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
    return render_template("signUp.html")

# About Page
@auth.route('/about')
def about():
    return render_template("about.html")

# user Page
@auth.route('/userPage.html')
def userPage():
     return render_template("userPage.html")