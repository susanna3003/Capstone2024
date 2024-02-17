import random
from flask import Blueprint, render_template, request, flash, redirect, url_for
import sqlite3

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
        password = request.form.get('password')
        passwordCon = request.form.get('passwordCon')

        # String input validations
        if len(email) < 4:
            flash('Email must be greater than 3 characters!', category='error')
        elif len(firstName) < 2:
            flash('First Name must be greater than 1 character!', category='error')
        elif password != passwordCon:
            flash('Passwords don\'t match!', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            # Connect to the database
            conn = sqlite3.connect('userDatabase.db')
            cur = conn.cursor()

            # Insert the user information into the database
            cur.execute("INSERT INTO users (firstname, email, userPass) VALUES (?, ?, ?)", (firstName, email, password))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            flash('Account created!', category='success')
    return render_template("signUp.html")

# About Page
@auth.route('/about')
def about():
    return render_template("about.html")

# Applications
@auth.route('/applications')
def applications():
    return render_template("applications.html")

# Calculator Application
@auth.route('/calculatorApp', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        # Handle calculation here
        try:
            expr = request.form['expression']
            result = eval(expr)
        except:
            result = 'E E E'
        return render_template('calculatorApp.html', result=result)
    return render_template('calculatorApp.html')

# Random Number Application [GET]
@auth.route('/randMathApp', methods=['GET'])
def get_randMathApp():
    # Declaring Variables
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*', '/'])
    question = f"{num1} {operator} {num2}"
    try: # Create Calculatons based on operator
        if operator == '+':
            correct_answer = num1 + num2
        elif operator == '-':
            correct_answer = num1 - num2
        elif operator == '*':
            correct_answer = num1 * num2
        elif operator == '/':
            correct_answer = num1 / num2
            correct_answer = round(correct_answer, 2)
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    return render_template("randMathApp.html", question=question, correct_answer = correct_answer)

# Random Number Application [POST]
@auth.route('/randMathApp', methods=['POST'])
def post_randMathApp():
    # Declaring variables
    user_answer = request.form.get("user_answer")
    correct_answer = request.form.get("correct_answer")
    result = " "
    try:
        if user_answer == correct_answer:
            result = "Correct!"
        else:
            result = "Incorrect. Try again."
    except ValueError: # user_answer did not contain an integer
        result = "Invalid number!"
    return render_template("randMathResult.html", correct_answer=correct_answer, result=result, user_answer=user_answer)

# Memory Bank
@auth.route('/memBankApp', methods=['GET', 'POST'])
def mem_bank_app():
    if request.method == 'POST':
        if 'equation' in request.form:
            equation = request.form['equation']
            equations.append(equation)
        elif 'clear' in request.form:
            # Handle clearing the list
            equations.clear()
        return redirect(url_for('auth.mem_bank_app'))  # Redirect to the same route after form submission
    return render_template('memBankApp.html')

@auth.route('/memBankDisplay')
def memBankDisplay():
    return render_template("memBankDisplay.html", equations=equations)