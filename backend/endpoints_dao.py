from backend.db_access import DatabaseAccess


class EndpointDAO:

    def __init__(self, db_name='monitor.db'):
        self.db = DatabaseAccess(db_name)
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        self.db.execute("""
                CREATE TABLE IF NOT EXISTS pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL UNIQUE,
                    hash TEXT,
                    check_interval INTEGER DEFAULT 300,
                    next_check INTEGER DEFAULT 0
                );
            """)

        self.db.execute("""
            CREATE TABLE IF NOT EXISTS changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id INTEGER NOT NULL,
                change_detected INTEGER NOT NULL,
                date INTEGER,
                FOREIGN KEY (page_id) REFERENCES pages(id) ON DELETE CASCADE
            );
        """)

    def get_all_endpoints(self):
        return self.db.fetch_all("SELECT * FROM pages ORDER BY id DESC")

    def insert_endpoint(self, url, interval, next_check):
        self.db.execute(
            "INSERT OR IGNORE INTO pages (url, check_interval, next_check) VALUES (?, ?, ?)",
            (url, interval, next_check)
        )

    def delete_endpoint(self, id):
        self.db.execute("DELETE FROM pages WHERE id = ?", (id,))

    def get_due_endpoints(self, current_time):
        return self.db.fetch_all(
            "SELECT * FROM pages WHERE next_check <= ?",
            (current_time,)
        )

    def update_check_result(self, page_id, new_hash, next_check_time):
        self.db.execute(
            "UPDATE pages SET hash = ?, next_check = ? WHERE id = ?",
            (new_hash, next_check_time, page_id)
        )

    def reschedule_check(self, page_id, next_check_time):
        self.db.execute(
            "UPDATE pages SET next_check = ? WHERE id = ?",
            (next_check_time, page_id)
        )

    def update_interval(self, page_id, interval):
        self.db.execute("UPDATE pages SET check_interval = ? WHERE id = ?", (interval, page_id))

    def add_change_record(self, page_id, change_detected, date):
        self.db.execute("INSERT INTO changes (page_id, change_detected, date) VALUES (?, ?, ?)",(page_id, change_detected, date))

    def get_changes(self, page_id):
        return self.db.fetch_all("SELECT * FROM changes WHERE page_id = ? ORDER BY date DESC", (page_id,))