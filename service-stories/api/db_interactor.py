import sqlite3
import os


class DB:

    def __init__(self, path: str):
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def _execute_query(self, query, params=()):
        """Executes a given SQL query with optional parameters."""
        self.cursor.execute(query, params)
        self.connection.commit()

    def _fetch_query(self, query, params=()):
        """Executes a given SQL query and returns fetched results."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def _create_table(self, create_table_sql):
        """Creates a table with the given SQL statement."""
        self._execute_query(create_table_sql)

    def _insert_data(self, insert_sql, data):
        """Inserts data into a table using the given SQL statement."""
        self._execute_query(insert_sql, data)

    def _query_data(self, query, params=()):
        """Queries data from the database."""
        return self._fetch_query(query, params)

    def __del__(self):
        self.connection.close()

    def get_stories(self):
        return self._fetch_query("SELECT * FROM `stories`")

    def add_story(self, story: dict):
        self._execute_query(
            "INSERT INTO `stories` (url, title, content, poster) VALUES (?, ?, ?, ?)",
            (story["url"], story["title"], story["content"], story["poster"]),
        )
