import sqlite3

def add_order():
    conn = sqlite3.connect("customer_support.db")
    cursor = conn.cursor()

    # Example order to insert
    new_order = (
        1,  # user_id (must match a valid user ID in 'users' table)
        "Smart Watch",  # product_name
        "Processing",   # status
        "2025-07-08",   # order_date
        "2025-07-12"    # delivery_date
    )

    cursor.execute("""
        INSERT INTO orders (user_id, product_name, status, order_date, delivery_date)
        VALUES (?, ?, ?, ?, ?)
    """, new_order)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ New order added.")

add_order()
