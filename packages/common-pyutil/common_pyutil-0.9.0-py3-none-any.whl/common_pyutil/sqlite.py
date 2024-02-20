import logging
from pathlib import Path
import sqlite3


class SQLite:
    def __init__(self, root_dir: Path | str, logger_name: str):
        self._root_dir = Path(root_dir)
        self.logger = logging.getLogger(logger_name)

    def database_name(self, database_name: str) -> str:
        return str(self._root_dir.joinpath(database_name))

    def backup(self, db_name: str):
        db_file = self.database_name(db_name)
        backup_file = self.database_name(db_name) + ".bak"
        conn = sqlite3.connect(db_file)
        backup = sqlite3.connect(backup_file)
        conn.backup(backup)
        backup.close()
        conn.close()

    def execute_sql(self, conn, cursor, query, params=None):
        try:
            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if cursor.description:
                column_names = [description[0] for description in cursor.description]
            else:
                column_names = None
            result = cursor.fetchall()
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Error {e} for query {query}")
            conn.close()
            return None, None
        return result, column_names

    def describe_table(self, database_name, table_name):
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        query = f"PRAGMA table_info({table_name})"
        # query = f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        result, column_names = self.execute_sql(conn, cursor, query)
        return result

    def create_table(self, database_name: str, table_name: str,
                     columns: list[str], pk: str | tuple | list):
        """Create a table named :code:`table_name` in a database

        Args:
            database_name: Database Name
            table_name: Table Name
            columns: List of column names
            pk: Primary Key

        Example:

            sql = SQLite("root_dir", "logger_name")
            sql.create_table("dbname", "table_name", ["col1", "col2"], "col1")


        """
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        if isinstance(pk, (tuple, list)):
            pk = ", ".join(pk)
            pk = f"({pk})".upper()
            _columns = ",".join([*[c.upper() for c in columns], f"primary key {pk}"])
        else:
            _columns = ",".join([c.upper() + " primary key" if c == pk.upper() else c.upper()
                                for c in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({_columns});"
        self.logger.debug(query)
        result, column_names = self.execute_sql(conn, cursor, query)
        return result

    def insert_many(self, database_name: str, table_name: str, data: list[dict]):
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        columns = data[0]
        keys = ",".join(k.upper() for k in columns.keys())
        vals = ','.join(['?'] * len(columns))
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({vals});"
        values = [[*d.values()] for d in data]
        try:
            result = cursor.executemany(query, values).fetchall()
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Error {e} for query {query}")
            conn.close()
            return None
        return result

    def insert_or_ignore_many(self, database_name: str, table_name: str, data: list[dict]):
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        columns = data[0]
        keys = ",".join(k.upper() for k in columns.keys())
        vals = ','.join(['?'] * len(columns))
        query = f"INSERT OR IGNORE INTO {table_name} ({keys}) VALUES ({vals});"
        values = [[*d.values()] for d in data]
        try:
            result = cursor.executemany(query, values).fetchall()
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Error {e} for query {query}")
            conn.close()
            return None
        return result

    def insert_data(self, database_name: str, table_name: str, data: dict):
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        keys = ",".join(k.upper() for k in data.keys())
        vals = ','.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({vals});"
        result, column_names = self.execute_sql(conn, cursor, query, [*data.values()])
        return result

    def update_data(self, database_name: str, table_name: str, data: dict, pk_name: str, pk):
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        keys = ", ".join(f"{k.upper()}=?" for k, v in data.items() if k.upper() != pk_name.upper())
        vals = [v for k, v in data.items() if k.upper() != pk_name.upper()]
        query = f"UPDATE {table_name} set {keys} where {pk_name.upper()} = ?;"
        params = tuple([*vals, pk])
        result, column_names = self.execute_sql(conn, cursor, query, params)
        return result

    def insert_or_ignore_data(self, database_name: str, table_name: str, data):
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        keys = ",".join(k.upper() for k in data.keys())
        vals = ','.join(['?'] * len(data))
        query = f"INSERT OR IGNORE INTO {table_name} ({keys}) VALUES ({vals});"
        result, column_names = self.execute_sql(conn, cursor, query, [*data.values()])
        return result

    def select_data(self, database_name, table_name, condition=None):
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        if condition:
            query = f"SELECT * FROM {table_name} WHERE {condition};"
        else:
            query = f"SELECT * FROM {table_name};"
        result, column_names = self.execute_sql(conn, cursor, query)
        return result, column_names

    def select_column(self, database_name, table_name, column, condition=None):
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        if condition:
            query = f"SELECT {column} FROM {table_name} WHERE {condition};"
        else:
            query = f"SELECT {column} FROM {table_name};"
        result, column_names = self.execute_sql(conn, cursor, query)
        return result

    def delete_many_rows(self, database_name: str, table_name: str, conditions: list[str]):
        try:
            conn = sqlite3.connect(self.database_name(database_name))
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION;")
            for condition in conditions:
                query = f"DELETE FROM {table_name} WHERE {condition}"
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.execute("COMMIT;")
            return result
        except Exception:
            cursor.execute("ROLLBACK;")
        return []

    def delete_rows(self, database_name, table_name, condition):
        conn = sqlite3.connect(self.database_name(database_name))
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name} WHERE {condition}"
        result, column_names = self.execute_sql(conn, cursor, query)
        return result
