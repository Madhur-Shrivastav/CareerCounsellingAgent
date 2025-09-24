import sqlite3

def connect_to_sqlite(db_name="customer_support.db"):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  
    return conn

def close_sqlite_connection(conn):
    if conn:
        conn.close()


