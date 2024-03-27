DROP INDEX IF EXISTS user_id_index;
DROP INDEX IF EXISTS user_name_index;
DROP INDEX IF EXISTS first_name_index;
DROP INDEX IF EXISTS second_name_index;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    first_name VARCHAR(255),
    second_name VARCHAR(255),
    password VARCHAR(255)
);

CREATE INDEX user_id_index ON users (user_id);
CREATE INDEX user_name_index ON users (user_name);
CREATE INDEX first_name_index ON users (first_name);
CREATE INDEX second_name_index ON users (second_name);
