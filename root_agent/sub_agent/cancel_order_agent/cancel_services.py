from datetime import datetime
from db import connect_to_sqlite, close_sqlite_connection
from google.adk.tools import ToolContext
import uuid

def cancel_order(id: str, reason: str, tool_context: ToolContext) -> str:
    """
    Cancels an order based on order ID.
    """
    cancellable_statuses = ["Pending", "Processing"]
    matched_order = None

    for order in tool_context.state.get("orders", []):
        if str(order["id"]) == str(id):  
            matched_order = order
            break

    if not matched_order:
        return "Provided order ID couldn't be matched."

    if matched_order["status"] not in cancellable_statuses:
        return (
            f"Order '{matched_order['product_name']}' is already "
            f"{matched_order['status'].lower()} and cannot be canceled."
        )

    update_order_status_in_db(matched_order["id"], reason=reason)

    return f"Order '{matched_order['product_name']}' has been successfully canceled."


def update_order_status_in_db(order_id: str, reason: str):
    conn = connect_to_sqlite()
    cursor = conn.cursor()
    cancellation_id = str(uuid.uuid4())
    request_date = datetime.utcnow().isoformat()
    status = "Cancelled"

    try:
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()

        cursor.execute("""
            INSERT INTO cancellations (id, order_id, reason, request_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, order_id, reason, request_date, status))
        conn.commit()
    finally:
        cursor.close()
        close_sqlite_connection(conn)
