import sqlite3
import time

def add_user():
    conn = sqlite3.connect("customer_support.db")
    cursor = conn.cursor()

    user_data = (
        "1",                             # id
        "Madhur Shrivastav",             # fullname
        "madhur",                        # username
        "madhur@icloud.com",             # email
        "9999900000",                     # contact
        "graduate",                       # education_level
        "password123",                    # password (hash in production)
        str(int(time.time() * 1000)),                    # timestamp
        str(int(time.time() * 1000))                     # lastlogin
    )

    cursor.execute("""
        INSERT INTO users (
            id, fullname, username, email, contact, education_level, password, timestamp, lastlogin
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, user_data)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ User added successfully.")


def drop_and_recreate_users_table():
    try:
        conn = sqlite3.connect("customer_support.db")
        cursor = conn.cursor()

        try:
            cursor.execute("DROP TABLE IF EXISTS users;")
            print("Successfully dropped 'users' table (if it existed).")
        except sqlite3.Error as e:
            print(f"Error dropping 'users' table: {e}")
            return 

        try:
            cursor.execute("""
                CREATE TABLE users (
                    id TEXT PRIMARY KEY,                            -- UUID
                    fullname TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    contact TEXT CHECK(length(contact) = 10),      -- 10-digit contact
                    education_level TEXT CHECK(education_level IN ('9th','10th','11th','12th','graduate')),
                    password TEXT NOT NULL,                          -- store hashed password
                    timestamp INTEGER NOT NULL,
                    lastlogin INTEGER NOT NULL
                );
            """)
            print("Successfully created 'users' table.")
            conn.commit() 
        except sqlite3.Error as e:
            print(f"Error creating 'users' table: {e}")
            conn.rollback() 

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

drop_and_recreate_users_table()
add_user()
