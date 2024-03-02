DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    taskID INTEGER PRIMARY KEY,
    userId INTEGER,
    name TEXT,
    taskType TEXT, 
    creationDate DATE, 
    deadline DATE, 
    description TEXT, 
    recurringTask INTEGER, 
    location TEXT, 
    FOREIGN KEY (userId) REFERENCES User(id)
);