import sqlite3

DB_NAME = "monitor.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS endpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT NOT NULL,
            html_text TEXT,
            last_check TEXT
        );
    """)

    conn.commit()
    conn.close()
    print("DB initialized.")

if __name__ == "__main__":
    init_db()
