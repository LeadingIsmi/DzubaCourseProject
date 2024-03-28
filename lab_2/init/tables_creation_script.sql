DROP INDEX IF EXISTS user_id_index;
DROP INDEX IF EXISTS user_name_index;
DROP INDEX IF EXISTS first_name_index;
DROP INDEX IF EXISTS second_name_index;
DROP INDEX IF EXISTS chat_id_index;
DROP INDEX IF EXISTS is_group_index;
DROP INDEX IF EXISTS members_id_index;
DROP INDEX IF EXISTS chat_members_id_index;

DROP TABLE IF EXISTS chat_members;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS chats;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE,
    first_name VARCHAR(255),
    second_name VARCHAR(255),
    password VARCHAR(255)
);
