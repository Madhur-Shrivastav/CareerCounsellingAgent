# import mysql.connector
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def connect_to_mysql():
#     try:
#         connection = mysql.connector.connect(
#             host=os.getenv("MYSQL_HOST"),
#             port=os.getenv("MYSQL_PORT"),
#             user=os.getenv("MYSQL_USER"),
#             password=os.getenv("MYSQL_PASSWORD"),
#             database=os.getenv("MYSQL_DATABASE")
#         )

#         if connection.is_connected():
#             print(f"MySQL connected to database: {os.getenv('MYSQL_DATABASE', 'customer_support')}")
#             return connection
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return None

# def close_mysql_connection(connection):
#     if connection and connection.is_connected():
#         connection.close()
#         print("MySQL connection closed")
import sqlite3

def connect_to_sqlite(db_name="customer_support.db"):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  
    return conn

def close_sqlite_connection(conn):
    if conn:
        conn.close()


