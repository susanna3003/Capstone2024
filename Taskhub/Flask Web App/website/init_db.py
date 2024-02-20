import sqlite3

connection = sqlite3.connect('userDatabase.db')
with open('schema.sql') as f:
        connection.executescript(f.read())
cur = connection.cursor()

cur.execute("INSERT INTO users (id, firstname, lastname, email, userPass, username, phoneNum) VALUES ('id', 'firstname', 'lastname', 'email', 'userPass', 'username', 'phoneNum')")
connection.commit()
connection.close()