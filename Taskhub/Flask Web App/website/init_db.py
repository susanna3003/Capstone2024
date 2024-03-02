import sqlite3

connection = sqlite3.connect('userDatabase.db')
with open('schema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()

        cur.execute("INSERT INTO users (id, firstname, lastname, email, userPass, username, phoneNum) VALUES ('id', 'firstname', 'lastname', 'email', 'userPass', 'username', 'phoneNum', 'accountType')")
        connection.commit()
        cur.execute("INSERT INTO Teacher (userId, teacherId, subjectTaught, qualifications) VALUES ('userId', 'teacherId', 'subjectTaught', 'qualifications')")
        connection.commit()
        cur.execute("INSERT INTO Parent (userId, parentId, childrenInfo) VALUES ('userId', 'parentId', 'childrenInfo')")
        connection.commit()
        cur.execute("INSERT INTO Student (userId, studentId, gradeLevel, coursesEnrolled) VALUES ('userId', 'studentId', 'gradeLevel', 'courseEnrolled')")
        connection.commit()
connection.close()

connection = sqlite3.connect('taskDatabase.db')
with open('taskSchema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()
        cur.execute("INSERT INTO tasks (taskID, userId, name, taskType, creationDate, deadline, description, recurringTask, location) VALUES ('taskID', 'id', 'name', 'taskType', 'creationDate', 'deadline', 'description', 'recurringTask', 'location')")
        connection.commit()
connection.close()