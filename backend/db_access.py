import sqlite3

class DatabaseAccess:
    _instance = None

    def __new__(cls, db_path='database.db'):
        if cls._instance is None:
            cls._instance = super(DatabaseAccess, cls).__new__(cls)
            cls._instance.db_path = db_path
        return cls._instance

    def _get_conn(self):
        return sqlite3.connect(
            self.db_path,
            timeout=5.0,
        )

    def execute(self, query, params=()):
        try:
            with self._get_conn() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
        except sqlite3.OperationalError as error:
            print(f"Database LOCKED Error (Execute): {error}")
            return None
        except Exception as error:
            print(f"Database error (Execute): {error}")
            return None

    def fetch_all(self, query, params=()):
        try:
            with self._get_conn() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError as error:
            print(f"Database LOCKED Error (Fetch All): {error}")
            return []
        except Exception as error:
            print(f"Database error (Fetch All): {error}")
            return []

    def fetch_one(self, query, params=()):
        try:
            with self._get_conn() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params)
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.OperationalError as error:
            print(f"Database LOCKED Error (Fetch One): {error}")
            return None
        except Exception as error:
            print(f"Database error (Fetch One): {error}")
            return None