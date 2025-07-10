import sqlite3
import uuid
# def add_cancellations():
#     conn = sqlite3.connect("customer_support.db")
#     cursor = conn.cursor()

#     new_order = (
#         str(uuid.uuid4()), 
#         1, 
#         "Iphone 13",  
#         "Processing",  
#         "2025-07-08",   
#         "2025-07-14"    
#     )

#     cursor.execute("""
#         INSERT INTO orders (id, user_id, product_name, status, order_date, delivery_date)
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, new_order)

#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("✅ New cancellation added.")

def drop_and_recreate_cancellations_table():
  
    try:
        conn = sqlite3.connect("customer_support.db")
        cursor = conn.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS cancellations;")
            print("Successfully dropped 'cancellations' table (if it existed).")
        except sqlite3.Error as e:
            print(f"Error dropping 'cancellations' table: {e}")
            return 

        try:
            cursor.execute("""
                CREATE TABLE cancellations (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    order_id TEXT,
                    product_name TEXT,
                    reason TEXT,
                    request_date TEXT
                );
            """)
            print("Successfully created 'cancellations' table with 'id' as TEXT and 'product_name' column.")
            conn.commit() 
        except sqlite3.Error as e:
            print(f"Error creating 'cancellations' table: {e}")
            conn.rollback() 

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

drop_and_recreate_cancellations_table()
# add_cancellations()
