DROP TABLE IF EXISTS weekReview;

CREATE TABLE weekReview (
    reviewID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER,
    reviewDate DATE,
    weekRating INTEGER,
    weekDesc TEXT,
    weekHigh TEXT,
    weekLow TEXT,
    weekComment TEXT,
    FOREIGN KEY (userId) REFERENCES User(id)
);