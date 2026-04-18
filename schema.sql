CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items(
    id INTEGER PRIMARY KEY,
    title TEXT,
    training_type TEXT,
    specialization TEXT,
    format TEXT,
    training_level TEXT,
    coach_id INTEGER REFERENCES users,
    training_date TEXT,
    training_time TEXT,
    training_description TEXT,
    user_id INTEGER REFERENCES users
);