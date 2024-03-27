from faker import Faker
from typing import Sequence, Mapping
import hashlib
import psycopg2.extras
from utils.postgres_connector import PostgresConnector

import psycopg2.extras


class PSQLManager:

    def create_tables(self, db_name: str) -> None:
        connector: PostgresConnector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        with open("./init/tables_creation_script.sql", "r") as tables_creation_cript:
            cursor.execute(tables_creation_cript.read())
        cursor.connection.commit()
        connector.close_connection()

    def insert_data_to_table(self, db_name: str, table_name: str, data: Sequence[Mapping]) -> None:
        connector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        columns = data[0].keys()
        columns_str = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES %s"
        data_to_insert = [[i[column] for column in columns] for i in data]
        psycopg2.extras.execute_values(cursor, sql, data_to_insert)
        cursor.connection.commit()
        connector.close_connection()

    def insert_connections(self, db_name: str, table_name: str, data: Sequence[Mapping]) -> None:
        connector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        columns = data[0].keys()
        columns_str = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES %s"
        data_to_insert = [[i[column] for column in columns] for i in data]
        psycopg2.extras.execute_values(cursor, sql, data_to_insert)
        cursor.connection.commit()
        connector.close_connection()


class DataFaker():

    def get_fake_users(self, count: int) -> Sequence[Mapping]:
        fake: Faker = Faker()
        users: Sequence[Mapping] = []
        for _ in range(count):
            user = self.create_fake_user(fake)
            users.append(user)
        return users

    def create_fake_user(self, fake: Faker) -> Mapping:
        user: dict = {}
        user_name: str = fake.unique.user_name()
        full_name: Sequence[str] = fake.unique.name().split()[:2]
        second_name: str = full_name[0]
        first_name: str = full_name[1]
        password: str = fake.unique.password()
        hashed_password: str = hashlib.sha256(password.encode()).hexdigest()
        user["user_name"], user["first_name"], user["second_name"], user["password"] = user_name, first_name, second_name, hashed_password
        return user
    
class Initializer:

    def init_data(self):
        print("Start initializing")
        db_worker = PSQLManager()
        db_name = "arch_db"
        creater_data = DataFaker()
        db_worker.create_tables(db_name)
        fake_users: Sequence[Mapping] = creater_data.get_fake_users(10)
        db_worker.insert_data_to_table(
            db_name=db_name, table_name="users", data=fake_users)

        print("Succesfully inited")


Initializer().init_data()
