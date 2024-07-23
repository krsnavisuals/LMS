DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS book_rented;
DROP TABLE IF EXISTS book_review;
DROP TABLE IF EXISTS section;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE section (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE,
    description TEXT,
    date VARCHAR(20)
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    author VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2),
    rented BOOLEAN DEFAULT 0,
    content TEXT,
    section VARCHAR(255),
    date_issued VARCHAR(20),
    return_date VARCHAR(20)
);

CREATE TABLE book_rented (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER UNIQUE,
    user_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES Books(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE book_review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    username VARCHAR(20),
    description TEXT
);
