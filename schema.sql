CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT DEFAULT 'client',
    image BLOB
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

CREATE TABLE participants(
    id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL REFERENCES items,
    user_id INTEGER NOT NULL REFERENCES users,
    UNIQUE (item_id, user_id)
);

CREATE TABLE images(
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    image BLOB
);

CREATE TABLE classes(
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT);
