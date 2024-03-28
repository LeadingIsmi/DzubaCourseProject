from datetime import datetime, timedelta
from faker import Faker
from typing import Sequence, Mapping
import hashlib
import random
import psycopg2.extras
import psycopg2
import time


class PostgresConnector:

    def __init__(self, db_name: str = 'postgres') -> None:
        self.db_name = db_name
        self.user = 'ismail'
        self.password = 'ismail'
        self.host = 'postgres'
        self.port = '5432'
        while True:
            try:
                self.conn = psycopg2.connect(dbname=self.db_name, user=self.user,
                                             password=self.password, host=self.host, port=self.port)
                break
            except Exception as e:
                print("Can't connect to postgres", e)
                time.sleep(5)

    def get_cursor(self) -> psycopg2.extensions.cursor:

        self.cur = self.conn.cursor()
        return self.cur

    def close_connection(self):
        self.cur.close()
        if self.conn:
            self.conn.close()


class PSQLManager:

    def create_tables(self, db_name: str) -> None:
        connector: PostgresConnector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        with open("./tables_creation_script.sql", "r") as tables_creation_cript:
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


class Initializer():

    @staticmethod
    def init_data(num_chats: int, users_count: int):
        print("Start initializing")
        Initializer.psql_init(users_count)
        print("Succesfully inited")

    @staticmethod
    def psql_init(users_count: int):
        print("Start initializing postgress")
        db_name = "shop_db"

        is_inited = False
        try:
            cursor = PostgresConnector(db_name=db_name).get_cursor()
            cursor.execute("SELECT * FROM users LIMIT 1;")
            is_inited = cursor.fetchone()
            if is_inited:
                print("Postgress already inited, skip initialization")
                return
        except:
            print("Not inited yet")
        finally:
            cursor.close()
            cursor.connection.close()
        db_worker = PSQLManager()
        db_worker.create_tables(db_name)
        fake_users: Sequence[Mapping] = Initializer.get_fake_users(
            users_count)
        db_worker.insert_data_to_table(
            db_name=db_name, table_name="users", data=fake_users)
        print("Succesfully inited postgress")

    @staticmethod
    def get_fake_users(count: int) -> Sequence[Mapping]:
        fake: Faker = Faker()
        users: Sequence[Mapping] = []
        for _ in range(count):
            user = Initializer.create_fake_user(fake)
            users.append(user)
        return users

    @staticmethod
    def create_fake_user(fake: Faker) -> Mapping:
        user: dict = {}
        user_name: str = fake.unique.user_name()
        full_name: Sequence[str] = fake.unique.name().split()[:2]
        second_name: str = full_name[0]
        first_name: str = full_name[1]
        password: str = fake.unique.password()
        hashed_password: str = hashlib.sha256(password.encode()).hexdigest()
        user["user_name"], user["first_name"], user["second_name"], user["password"] = user_name, first_name, second_name, hashed_password
        return user

    @staticmethod
    def random_date(start_date, end_date):
        time_between_dates = end_date - start_date
        random_number_of_days = random.randrange(time_between_dates.days)
        random_date = start_date + timedelta(days=random_number_of_days)
        return random_date


num_chats: int = 100
users_count: int = 10000
Initializer().init_data(num_chats=num_chats, users_count=users_count)
