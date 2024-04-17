DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    taskID INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER,
    taskName TEXT,
    taskType TEXT, 
    creationDate DATE, 
    dateDue DATE, 
    description TEXT, 
    recurringTask TEXT, 
    location TEXT, 
    FOREIGN KEY (userId) REFERENCES User(id)
);

DROP TABLE IF EXISTS reminders;

CREATE TABLE reminders (
    reminderID INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER,
    reminderName TEXT,
    reminderType TEXT, 
    creationDate DATE, 
    dateDue DATE, 
    description TEXT, 
    recurringReminder TEXT, 
    location TEXT, 
    FOREIGN KEY (userId) REFERENCES User(id)
);