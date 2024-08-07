import sqlite3
from sqlite3 import Connection

DATABASE_NAME = "images.db"

def get_db_connection() -> Connection:
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     filename TEXT NOT NULL,
     upload_time DATETIME NOT NULL)
    ''')
    conn.commit()
    conn.close()