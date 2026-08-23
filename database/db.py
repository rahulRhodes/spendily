import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "expense_tracker.db")

SEED_EXPENSES = [
    # category, amount, day offset, description
    ("Food", 54.30, 1, "Grocery shopping"),
    ("Transport", 20.00, 4, "Metro card top-up"),
    ("Bills", 85.00, 7, "Electricity bill"),
    ("Health", 18.75, 10, "Pharmacy - medicines"),
    ("Entertainment", 24.50, 13, "Movie tickets"),
    ("Shopping", 62.99, 16, "New shoes"),
    ("Other", 15.00, 19, "Miscellaneous"),
    ("Food", 38.20, 22, "Dinner with friends"),
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()

    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123", method="pbkdf2:sha256")),
    )
    user_id = cursor.lastrowid

    today = date.today()
    for category, amount, day_offset, description in SEED_EXPENSES:
        expense_date = date(today.year, today.month, day_offset).isoformat()
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, expense_date, description),
        )

    conn.commit()
    conn.close()
