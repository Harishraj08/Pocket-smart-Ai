import sqlite3
from pathlib import Path
from contextlib import contextmanager
from .config import get_settings

def db_path():
    p=Path(get_settings().database_path)
    if not p.is_absolute(): p=Path.cwd()/p
    p.parent.mkdir(parents=True,exist_ok=True)
    return p

def init_db():
    with sqlite3.connect(db_path()) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT UNIQUE NOT NULL,name TEXT NOT NULL,
          password_hash TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("""CREATE TABLE IF NOT EXISTS recommendations(
          id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,planner TEXT NOT NULL,budget REAL NOT NULL,
          request_json TEXT NOT NULL,response_json TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(user_id) REFERENCES users(id))""")
        c.commit()

@contextmanager
def get_conn():
    c=sqlite3.connect(db_path()); c.row_factory=sqlite3.Row
    try: yield c; c.commit()
    finally: c.close()
