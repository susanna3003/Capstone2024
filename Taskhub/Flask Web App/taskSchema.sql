DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    taskID INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER,
    name TEXT,
    taskType TEXT, 
    creationDate DATE, 
    deadline DATE, 
    description TEXT, 
    recurringTask TEXT, 
    location TEXT, 
    FOREIGN KEY (userId) REFERENCES User(id)
);