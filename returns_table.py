import sqlite3
def drop_and_recreate_returns_table():
  
    try:
        conn = sqlite3.connect("customer_support.db")
        cursor = conn.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS returns;")
            print("Successfully dropped 'returns' table (if it existed).")
        except sqlite3.Error as e:
            print(f"Error dropping 'returns' table: {e}")
            return 

        try:
            cursor.execute("""
                CREATE TABLE returns (
                    id TEXT PRIMARY KEY,             
                    user_id INTEGER NOT NULL,         
                    order_id TEXT NOT NULL,           
                    product_name TEXT NOT NULL,       
                    reason TEXT NOT NULL,             
                    request_date TEXT NOT NULL,       
                    status TEXT NOT NULL DEFAULT 'Return Requested'  
                );
            """)
            print("Successfully created 'returns' table with 'id' as TEXT and 'product_name' column.")
            conn.commit() 
        except sqlite3.Error as e:
            print(f"Error creating 'returns' table: {e}")
            conn.rollback() 

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

drop_and_recreate_returns_table()


