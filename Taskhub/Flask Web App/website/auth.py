import uuid, sqlite3, re
from flask import Blueprint, session, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Message
from datetime import date
from datetime import datetime, timedelta
from website import mail

auth = Blueprint('auth', __name__)

#   Login Page
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

#   SignUp page
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
        elif len(password) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif not re.match(r'^(\d{10}|\d{3}-\d{3}-\d{4})$', phoneNum):
            flash('Phone number must be in the format XXX-XXX-XXXX or XXXXXXXXXX', category='error')
        else:
            # Connect to the database
            conn = sqlite3.connect('userDatabase.db')
            cur = conn.cursor()

            # Checking if email is already in use. 
            cur.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
            existing_email_count = cur.fetchone()[0]
            if existing_email_count > 0:
                flash('Email already exists. Please choose a different email address.', category='error')
            else:
                # Insert the user information into the database
                cur.execute("INSERT INTO users (firstname, lastName, email, userPass, username, phoneNum, accountType) VALUES (?, ?, ?, ?, ?, ?, ?)", (firstName, lastName, email, password, username, phoneNum, accountType))
                user_id = cur.lastrowid  # Get the ID of the inserted user
                session['id'] = user_id
                conn.commit()
                flash('Account created!', category='success')
                session['logged_in'] = True
                session['show_account_type_popup'] = True
                conn.close()
                return redirect(url_for("auth.userPage"))
    return render_template("signUp.html")
    
#   About Page
@auth.route('/about')
def about():
    return render_template("about.html")

#   user Page
@auth.route('/userPage', methods=['GET','POST'])
def userPage():
    user_id = session.get('id')
    conn = sqlite3.connect('userDatabase.db')
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user_data = cur.fetchone()
    conn.close()
    username = user_data[0] if user_data else "User"
    disableBtn = False
    show_account_type_popup = session.get('show_account_type_popup', False)
    
    #   Check when user submitted weekly Review
    if user_id:
        conn = sqlite3.connect('weekReview.db')
        cur = conn.cursor()
        cur.execute("SELECT MAX(submissionDate) FROM weekReview WHERE userId = ?", (user_id,))
        submissionDate = cur.fetchone()[0]
        conn.close()
        if submissionDate:
            submissionDate = datetime.strptime(submissionDate, '%Y-%m-%d')
            if submissionDate + timedelta(days=7) > datetime.now():
                disableBtn = True
    return render_template("userPage.html", show_account_type_popup=show_account_type_popup, username = username, disableBtn=disableBtn)

# Week Review viewer
@auth.route('/viewWeekReview')
def viewWeekReview():
    return render_template("viewWeekReview.html")

# retireving week Reviews
@auth.route('/getReviews')
def getReviews():
    user_id = session.get('id')
    conn = sqlite3.connect('weekReview.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM weekReview WHERE userId = ?", (user_id,))
    reviewsData = cur.fetchall()
    conn.close()
    reviews = []
    for review in reviewsData:
        reviewDictionary = {
            'date': review[2],  # date
            'rating': review[3],  # review rating
            'description': review[4],  # review description
            'weekHigh': review[5],  # review high
            'weekLow': review[6],  # review low
            'comment': review[7],  # review comment
        }
        reviews.append(reviewDictionary)
    return jsonify(reviews)

#   account type Route/account creaction
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
        cur.execute("INSERT INTO Teacher (userId, teacherId) VALUES (?, ?)", (user_id, generate_unique_teacher_id()))
    elif accountType == 'parent':
        cur.execute("INSERT INTO Parent (userId, parentId) VALUES (?, ?)", (user_id, generate_unique_parent_id()))
    elif accountType == 'student':
        cur.execute("INSERT INTO Student (userId, studentId) VALUES (?, ?)", (user_id, generate_unique_student_id()))
    conn.commit()
    conn.close()
    session['show_account_type_popup'] = False # Prevents pop up loop
    return redirect(url_for('auth.userPage'))

#   Generating unique ID for account type
def generate_unique_teacher_id():
    # Generate a unique ID for the teacher
    teacherId = str(uuid.uuid4())
    return teacherId
def generate_unique_parent_id():
    # Generate a unique ID for the teacher
    parentId = str(uuid.uuid4())
    return parentId
def generate_unique_student_id():
    # Generate a unique ID for the teacher
    studentId = str(uuid.uuid4())
    return studentId

#   Logout route
@auth.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear the session variable
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout

#   Calendar Route
@auth.route('/calendar')
def calendar():
    return render_template("calendar.html")

#   Retrieving tasks
@auth.route('/getTasks')
def get_tasks():
    user_id = session.get('id')
    conn = sqlite3.connect('taskDatabase.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE userId = ?", (user_id,))
    tasks = cur.fetchall()
    conn.close()
    events = []
    for task in tasks:
        event = {
            'id': task[0],  # Task ID
            'title': task[2],  # Task name
            'start': task[5],  # Task deadline
            'description': task[6],  # Task description
        }
        events.append(event)
    return jsonify(events)

#   Preferences Route
@auth.route('/preferences')
def preferences():
    return render_template("preferences.html")

#   Privacy Route
@auth.route('/privacy')
def privacy():
    return render_template("privacy.html")

#   Account Deletion Route
@auth.route('/delete-account', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        user_id = session.get('id')

        # Delete the user's account from the database
        conn = sqlite3.connect('userDatabase.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        cur.execute("DELETE FROM Student WHERE userId = ?", (user_id,))
        cur.execute("DELETE FROM Parent WHERE userId = ?", (user_id,))
        cur.execute("DELETE FROM Teacher WHERE userId = ?", (user_id,))
        conn.close()
        conn = sqlite3.connect('taskDatabase.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE userId = ?", (user_id,))
        conn.commit()
        conn.close()

        conn = sqlite3.connect('weekReview.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM weekReview WHERE userId = ?", (user_id,))
        conn.commit()
        conn.close()

        # Clear the session
        session.clear()

        # Redirect the user to the home page
        # Flash a message to indicate that their account  has been updated
        flash('Your account has successfully been deleted! Goodbye!', 'success')
    return redirect(url_for('views.home'))

#   Update Password Route
@auth.route('/updatePass', methods=['POST'])
def update_pass():
    if request.method == 'POST':
        user_id = session.get('id')
        newPassword = request.form.get('newPass')
        currentPassword = request.form.get('currPass')

        # Connect to the database and update password
        conn = sqlite3.connect('userDatabase.db')
        cur = conn.cursor()
        cur.execute("SELECT userPass FROM users WHERE id = ?", (user_id,))
        storedPassword = cur.fetchone()[0]

        # Determine if current password matches database password before changing
        if currentPassword == storedPassword:
            # Update the password in the database
            cur.execute("UPDATE users SET userPass = ? WHERE id = ?", (newPassword, user_id))
            conn.commit()
            conn.close()

            # Flash a success message
            flash('Your password has been updated successfully!', 'success')
            return redirect(url_for('auth.userPage'))
        else:
            # Flash an error message
            flash('Incorrect current password. Please try again.', 'error')
            return redirect(url_for('auth.privacy'))
    return "Method Not Allowed", 405

#   Update email route
@auth.route('/updateEmail', methods=['POST'])
def updateEmail():
    if request.method == 'POST':
        user_id = session.get('id')
        new_email = request.form.get('newEmail')

        # Connect to the database and update email
        conn = sqlite3.connect('userDatabase.db')
        cur = conn.cursor()
        cur.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
        conn.commit()
        conn.close()

        # Flash a message to indicate that the password has been updated
        flash('Your email has been updated successfully!', 'success')
    # Redirect the user back to the user page
    return redirect(url_for('auth.userPage'))

# Task Home
@auth.route('/taskHome', methods=['GET', 'POST'])
def taskHome():
    if request.method == 'POST':
        userID = session.get('id')
        taskName = request.form.get('taskName')
        taskType = request.form.get('taskType')
        dateDue = request.form.get('dateDue')
        dateCreated = date.today()
        description = request.form.get('taskDescription')
        location = request.form.get('taskLocation')
        invites = request.form.get('taskInvite')
        reminder = request.form.get('taskRemind')
        recurringTask = request.form.get('taskRecurr')

        # Connect to the database
        conn = sqlite3.connect('taskDatabase.db')
        cur = conn.cursor()

        # Insert the user information into the database
        cur.execute("INSERT INTO tasks (userId, taskName, taskType, creationDate, dateDue, description, recurringTask, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (userID, taskName, taskType, dateCreated, dateDue, description, recurringTask, location))

        # Commit the changes and close the connection
        conn.commit()
        flash('Task created!', category='success')
        session['logged_in'] = True
        conn.close()
        return redirect(url_for('auth.calendar'))
    return render_template("taskHome.html")
    
# Reminder Home
@auth.route('/reminderHome')
def reminderHome():
    return render_template("reminderHome.html")

# Week Review
@auth.route('/weekReview', methods=['GET', 'POST'])
def weekReview():
    if request.method == 'POST':
        userID = session.get('id')
        submissionDate = date.today()
        weekRating = request.form.get('weekRating')
        weekDesc = request.form.get('weekDesc')
        weekHigh = request.form.get('weekHigh')
        weekLow = request.form.get('weekLow')
        weekComment = request.form.get('weekComment')

        # Connect to weekReview database
        conn = sqlite3.connect('weekReview.db')
        cur = conn.cursor()

        # Insert the user information into the database
        cur.execute("INSERT INTO weekReview (userID, submissionDate, weekRating, weekDesc, weekHigh, weekLow, weekComment) VALUES (?, ?, ?, ?, ?, ?, ?)", (userID, submissionDate, weekRating, weekDesc, weekHigh, weekLow, weekComment))

        # Commit the changes and close the connection
        conn.commit()
        flash('Review Complete!', category='success')
        conn.close()
        return redirect(url_for('auth.userPage'))
    return render_template("weekReview.html")

   #!!!!! Forgot Password Group !!!!!!#
# Forgot Password Route
@auth.route('/forgotPassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user_email = request.form.get('userEmail')
        if emailDatabaseCheck(user_email):
            passwordResetEmail(user_email)
            flash('An email with instructions to reset your password has been sent.', 'info')
            return redirect(url_for('auth.login'))
        else:
            # If the email doesn't exist in the database, show an error message
            flash('Email not found. Please enter a valid email address.', 'error')
            return render_template("forgotPassword.html")
    else:
        # Render the forgot password form
        return render_template("forgotPassword.html")
    
# Function to check if email exists in the database
def emailDatabaseCheck(email):
    conn = sqlite3.connect('userDatabase.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    return user is not None

# Send password reset email
def passwordResetEmail(email):
    msg = Message('Password Reset', sender='luckyfoot028@gmail.com"', recipients=[email])
    msg.subject = "Taskhub Password Reset"
    msg.body = 'Click the following link to reset your password: http://127.0.0.1:5000/passwordReset'
    mail.send(msg)