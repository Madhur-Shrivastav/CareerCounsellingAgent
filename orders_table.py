import sqlite3
import uuid
def add_order():
    conn = sqlite3.connect("customer_support.db")
    cursor = conn.cursor()

    new_order = (
        str(uuid.uuid4()), 
        1, 
        "Iphone 13",  
        "Processing",  
        "2025-07-08",   
        "2025-07-14"    
    )

    cursor.execute("""
        INSERT INTO orders (id, user_id, product_name, status, order_date, delivery_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, new_order)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ New order added.")

def drop_and_recreate_order_table():
  
    try:
        conn = sqlite3.connect("customer_support.db")
        cursor = conn.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS orders;")
            print("Successfully dropped 'orders' table (if it existed).")
        except sqlite3.Error as e:
            print(f"Error dropping 'orders' table: {e}")
            return 

        try:
            cursor.execute("""
                CREATE TABLE orders (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    product_name TEXT,
                    status TEXT,
                    order_date TEXT,
                    delivery_date TEXT
                );
            """)
            print("Successfully created 'orders' table with 'id' as TEXT and 'product_name' column.")
            conn.commit() 
        except sqlite3.Error as e:
            print(f"Error creating 'orders' table: {e}")
            conn.rollback() 

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# drop_and_recreate_order_table()
add_order()
