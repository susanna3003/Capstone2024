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