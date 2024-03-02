import uuid
from flask import Blueprint, app, session, render_template, request, flash, redirect, url_for
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
                session['logged_in'] = True
                session['id'] = user[0]
                conn.close()
                return redirect(url_for("auth.userPage"))
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
        accountType = request.form.get('selectedAccountType')
        
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
            cur.execute("INSERT INTO users (firstname, lastName, email, userPass, username, phoneNum, accountType) VALUES (?, ?, ?, ?, ?, ?, ?)", (firstName, lastName, email, password, username, phoneNum, accountType))
            user_id = cur.lastrowid  # Get the ID of the inserted user
            session['id'] = user_id

            # Commit the changes and close the connection
            conn.commit()
            flash('Account created!', category='success')
            session['logged_in'] = True
            session['show_account_type_popup'] = True
            conn.close()
            return redirect(url_for("auth.userPage"))
    return render_template("signUp.html")

# About Page
@auth.route('/about')
def about():
    return render_template("about.html")

# user Page
@auth.route('/userPage')
def userPage():
    # Check if the user's account type is set
    user_id = session.get('id')
    conn = sqlite3.connect('userDatabase.db')
    cur = conn.cursor()
    cur.execute("SELECT accountType FROM users WHERE id = ?", (user_id,))
    cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user_data = cur.fetchone()
    username = user_data[0] if user_data else "User"
    conn.close()
    show_account_type_popup = session.get('show_account_type_popup', False)
    return render_template("userPage.html", show_account_type_popup=show_account_type_popup, username=username)

# account type Route/account creaction
@auth.route('/save_account_type', methods=['POST'])
def save_account_type():
    # Retrieve the selected account type from the form
    accountType = request.form.get('accountType')

    # Get the user's ID
    user_id = session.get('id')

    # Connect to the database
    conn = sqlite3.connect('userDatabase.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET accountType = ? WHERE id = ?", (accountType, user_id))
    conn.commit()

    # Linking user account type to specific database
    if accountType == 'teacher':
        cur.execute("INSERT INTO Teacher (id, teacher_id) VALUES (?, ?)", (user_id, generate_unique_teacher_id()))
    elif accountType == 'parent':
        cur.execute("INSERT INTO Parent (id, parent_id) VALUES (?, ?)", (user_id, generate_unique_parent_id()))
    elif accountType == 'student':
        cur.execute("INSERT INTO Student (id, student_id) VALUES (?, ?)", (user_id, generate_unique_student_id()))
    conn.commit()
    conn.close()
    session['show_account_type_popup'] = False # Prevents pop up loop
    return redirect(url_for('auth.userPage'))

# Generating unique ID for account type
def generate_unique_teacher_id():
    # Generate a unique ID for the teacher
    teacher_id = str(uuid.uuid4())
    return teacher_id
def generate_unique_parent_id():
    # Generate a unique ID for the teacher
    teacher_id = str(uuid.uuid4())
    return teacher_id
def generate_unique_student_id():
    # Generate a unique ID for the teacher
    teacher_id = str(uuid.uuid4())
    return teacher_id

# Logout route
@auth.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear the session variable
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout

# Calendar Route
@auth.route('/calendar')
def calendar():
    return render_template("calendar.html")