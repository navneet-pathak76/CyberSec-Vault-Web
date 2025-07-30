import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'vault.db')

def init_db():
    # Always connect and ensure the credentials table exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_credential(website, encrypted_password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO credentials (website, password) VALUES (?, ?)",
        (website, encrypted_password)
    )
    conn.commit()
    conn.close()

def get_credentials():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, website, password FROM credentials")
    credentials = [
        {'id': row[0], 'website': row[1], 'password': row[2]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return credentials
