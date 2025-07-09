from datetime import datetime
from db import connect_to_sqlite, close_sqlite_connection
from google.adk.tools import ToolContext

def raise_complaint(order_id: str, description: str , tool_context: ToolContext = None) -> str:
    """
    Raises a complaint and logs it both in the database and in the state.
    """

    created_at = datetime.now()
    complaint_ref = f"CPL-{created_at.strftime('%Y%m%d%H%M%S')}"
    status = "Pending"

    conn = connect_to_sqlite()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO complaints (user_id, order_id, description, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (tool_context.state["user_id"], order_id, description, status, created_at.date().isoformat()))
        conn.commit()
    except Exception as e:
        return f"Failed to submit complaint: {str(e)}"
    finally:
        cursor.close()
        close_sqlite_connection(conn)

    return (
        f"I'm really sorry to hear that. I've logged your complaint"
        f"{' for Order ID ' + str(order_id) if order_id else ''} with reference number {complaint_ref}. "
        f"Our support team will get back to you within 48 hours."
    )
