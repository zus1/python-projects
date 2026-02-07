from enum import Enum
import dotenv
import os

from config import Config

class DatabaseType(Enum):
    mysql = 'mysql'
    postgresql = 'pgsql'
    sqlite = 'sqlite'

class Connection:
    def __init__(self):
        self.conn = None

    def connect(self):
        if not self.conn:
            dotenv.load_dotenv()
            connection_type = os.environ.get("DB_TYPE")

            if connection_type == DatabaseType.mysql.value:
                self.__connect_mysql()
            if connection_type == DatabaseType.postgresql.value:
                self.__connect_postgresql()
            if connection_type == DatabaseType.sqlite.value:
                self.__connect_sqlite()

            if not self.conn:
                raise Exception('Unknown database connection type')

        return self.conn

    def close(self):
        self.conn.close()

    def __connect_mysql(self):
        import mysql.connector as mysql

        self.conn = mysql.connect(
            **Connection.__connection_dictionary(),
            port=os.environ.get("DB_PORT", 3306),
            charset=os.environ.get("DB_CHARSET", "utf8mb"),
            use_unicode=True,
            ssl_disabled=False,
        )

    def __connect_postgresql(self):
        import psycopg2

        self.conn = psycopg2.connect(
            **Connection.__connection_dictionary(),
            port=os.environ.get("DB_PORT", 5432),
            sslmode='disable',
        )

    def __connect_sqlite(self):
        import sqlite3

        self.conn = sqlite3.connect('csv_import.db')

    @staticmethod
    def __connection_dictionary():
        return {
            'host': os.environ.get("DB_HOST", "localhost"),
            'user': os.environ.get("DB_USER"),
            'password': os.environ.get("DB_PASSWORD"),
            'database': os.environ.get("DB_NAME"),
        }

    def reset(self):
        self.conn.close()
        self.conn = None


class Database:
    def __init__(self):
        dotenv.load_dotenv()

        self.connection = Connection().connect()
        self.table = os.environ.get("DB_TABLE")

    def import_csv(self, rows: list[tuple]):
        title_row, title_row_str = Database.__determine_title_line(rows)

        values_placeholders = Database.__determine_placeholders(title_row=title_row)

        self.__create_table(title_row_str)

        sql = f'INSERT INTO {self.table} ({title_row_str}) VALUES ({values_placeholders})'

        cursor = self.connection.cursor()

        cursor.executemany(sql, rows)
        self.connection.commit()

        rows_inserted = cursor.rowcount
        print(f'Inserted {rows_inserted} rows of {len(rows)} into {self.table}\n')

        if rows_inserted != len(rows):
            print(f'{len(rows) - rows_inserted} rows could not be inserted')

        self.connection.close()

    @staticmethod
    def __determine_title_line(rows: list[tuple])->tuple[list[str], str]:
        title_row_from_config = Config.get_title_line()

        title_row = title_row_from_config if title_row_from_config else rows.pop(0)
        title_row_str = ','.join(title_row)

        return title_row, title_row_str

    @staticmethod
    def __determine_placeholders(title_row: list)->str:
        connection_type = os.environ.get("DB_TYPE")

        if connection_type == DatabaseType.sqlite.value:
            return ('?,' * len(title_row))[:-1]

        return ('%s,' * len(title_row))[:-1]

    def __create_table(self, title_line: str):
        connection_type = os.environ.get("DB_TYPE")

        if connection_type == DatabaseType.sqlite.value:
            cursor = self.connection.cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table} ({title_line})')


