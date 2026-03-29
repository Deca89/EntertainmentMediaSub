CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    link TEXT,
    media_type TEXT,
    descriptions TEXT,
    user_id INTEGER REFERENCES users
)