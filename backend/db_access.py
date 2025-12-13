import sqlite3

class DatabaseAccess:
    _instance = None

    def __new__(cls, db_path='database.db'):
        if cls._instance is None:
            cls._instance = super(DatabaseAccess, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(db_path, check_same_thread=False)
            cls._instance.connection.row_factory = sqlite3.Row #objects that can be converted to dictionaries
        return cls._instance

    def execute(self, query, params=()):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as error:
            print(f"Database error: {error}")
            return None

    def fetch_all(self, query, params=()):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        except Exception as error:
            print(f"Database error: {error}")
            return []

    def fetch_one(self, query, params=()):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as error:
            print(f"Database error: {error}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()