import sqlite3



connection = sqlite3.connect('taskDatabase.db')
with open('taskSchema.sql') as f:
        connection.executescript(f.read())
        cur = connection.cursor()
        cur.execute("INSERT INTO tasks (userId, name, taskType, creationDate, deadline, description, recurringTask, location) VALUES ('id', 'name', 'taskType', 'creationDate', 'deadline', 'description', 'recurringTask', 'location')")
        connection.commit()
connection.close()