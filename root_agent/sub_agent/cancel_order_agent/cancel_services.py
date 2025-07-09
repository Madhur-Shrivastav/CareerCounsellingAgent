from datetime import datetime
from db import connect_to_sqlite, close_sqlite_connection
from google.adk.tools import ToolContext

def cancel_order(id: str, tool_context: ToolContext) -> str:
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

    matched_order["status"] = "Cancelled"
    update_order_status_in_db(matched_order["id"], "Cancelled")

    # interaction_log = {
    #     "timestamp": datetime.now().isoformat(),
    #     "type": "cancel_order",
    #     "id": matched_order["id"],
    #     "message": f"Order '{matched_order['product']}' was canceled."
    # }

    return f"Order '{matched_order['product_name']}' has been successfully canceled."



def update_order_status_in_db(id: str, status: str):
    conn = connect_to_sqlite()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, id))
        conn.commit()
    finally:
        cursor.close()
        close_sqlite_connection(conn)
