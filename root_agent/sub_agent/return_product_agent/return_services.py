from datetime import datetime, timezone
from db import connect_to_sqlite, close_sqlite_connection
from google.adk.tools import ToolContext
import uuid

def return_order(id: str, reason: str, tool_context: ToolContext) -> str:
    """
    Processes a return request for a delivered order.
    """
    matched_order = None

    for order in tool_context.state.get("orders", []):
        if str(order["id"]) == str(id):
            matched_order = order
            break

    if not matched_order:
        return "Provided order ID couldn't be matched."

    if matched_order["status"] != "Delivered":
        return (
            f"Order '{matched_order['product_name']}' is not eligible for return. "
            f"Its current status is '{matched_order['status']}'."
        )

    log_return_request(
        order_id=matched_order["id"],
        user_id=tool_context.state["user_id"],
        product_name=matched_order["product_name"],
        reason=reason
    )

    return f"✅ Return request for '{matched_order['product_name']}' has been successfully submitted."


def log_return_request(order_id: str, user_id: int, product_name: str, reason: str):
    """
    Logs the return request in the database and updates the order status to 'Return Requested'.
    """
    conn = connect_to_sqlite()
    cursor = conn.cursor()
    return_id = str(uuid.uuid4())
    request_date = datetime.now(timezone.utc).date().isoformat()

    try:
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", ("Return Requested", order_id))
        conn.commit()

        cursor.execute("""
            INSERT INTO returns (id, user_id, order_id, product_name, reason, request_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (return_id, user_id, order_id, product_name, reason, request_date, "Return Requested"))
        conn.commit()

    finally:
        cursor.close()
        close_sqlite_connection(conn)
