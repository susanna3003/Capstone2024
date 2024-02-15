DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id int AUTO_INCREMENT Primary Key,
    firstname VARCHAR2(15) NOT NULL,
    email VARCHAR2(30) NOT NULL,
    userPass VARCHAR2(7) NOT NULL
);