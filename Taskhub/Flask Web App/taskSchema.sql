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
    invitees TEXT, 
    location TEXT, 
    FOREIGN KEY (userId) REFERENCES User(id)
);

DROP TABLE IF EXISTS reminders;
CREATE TABLE reminders (
    reminderID INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER,
    reminderName TEXT, 
    creationDate DATE, 
    reminderDate DATE, 
    reminderDesc TEXT, 
    recurringReminder TEXT, 
    location TEXT, 
    FOREIGN KEY (userId) REFERENCES User(id)
);