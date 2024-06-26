import sqlite3

connection = sqlite3.connect('userDatabase.db')
with open('schema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()
        cur.execute("INSERT INTO users (firstname, lastname, email, userPass, username, phoneNum, accountType, profilePicturePath) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", ('firstname', 'lastname', 'email', 'userPass', 'username', 'phoneNum', 'accountType', 'profilePicturePath'))
        connection.commit()
        cur.execute("INSERT INTO Teacher (userId, teacherId, subjectTaught) VALUES (?, ?, ?)", ('userId', 'teacherId', 'subjectTaught'))
        connection.commit()
        cur.execute("INSERT INTO Parent (userId, parentId, childrenInfo) VALUES (?, ?, ?)", ('userId', 'parentId', 'childrenInfo'))
        connection.commit()
        cur.execute("INSERT INTO Student (userId, studentId, gradeLevel, coursesEnrolled) VALUES (?, ?, ?, ?)", ('userId', 'studentId', 'gradeLevel', 'courseEnrolled'))
        connection.commit()
connection.close()

connection = sqlite3.connect('taskDatabase.db')
with open('taskSchema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()
        cur.execute("INSERT INTO tasks (userId, taskName, taskType, creationDate, dateDue, description, recurringTask, invitees, location) VALUES ('id', 'taskName', 'taskType', 'creationDate', 'dateDue', 'description', 'recurringTask', 'invitees', 'location')")
        connection.commit()
connection.close()

connection = sqlite3.connect('taskDatabase.db')
with open('taskSchema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()
        cur.execute("INSERT INTO reminders (userId, reminderName, creationDate, reminderDate, reminderDesc, recurringReminder, location) VALUES ('id', 'reminderName', 'creationDate', 'reminderDate', 'reminderDesc', 'recurringReminder', 'location')")
        connection.commit()
connection.close()

connection = sqlite3.connect('weekReview.db')
with open('weekReview.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()
        cur.execute("INSERT INTO weekReview (userID, submissionDate, weekRating, weekDesc, weekHigh, weekLow, weekComment) VALUES (?, ?, ?, ?, ?, ?,?)", ('userID', 'submissionDate', 'weekRating', 'weekDesc', 'weekHigh', 'weekLow', 'weekComment'))
        connection.commit()
connection.close()
