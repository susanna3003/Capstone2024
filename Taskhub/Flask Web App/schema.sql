DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname VARCHAR(15) NOT NULL,
    lastname VARCHAR(15) NOT NULL,
    email VARCHAR(30) NOT NULL,
    userPass VARCHAR(12) NOT NULL,
    username VARCHAR(12) NOT NULL,
    phoneNum VARCHAR(15) NOT NULL,
    accountType VARCHAR(15),
    profilePicturePath VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Teacher (
    userId INTEGER PRIMARY KEY,
    teacherId INTEGER UNIQUE,
    subjectTaught TEXT,
    FOREIGN KEY (userId) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Parent (
    userId INTEGER PRIMARY KEY,
    parentId INTEGER UNIQUE,
    childrenInfo TEXT,
    FOREIGN KEY (userId) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Student (
    userId INTEGER PRIMARY KEY,
    studentId INTEGER UNIQUE,
    gradeLevel TEXT,
    coursesEnrolled TEXT,
    FOREIGN KEY (userId) REFERENCES User(id)
);