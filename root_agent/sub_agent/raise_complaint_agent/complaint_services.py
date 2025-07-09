from datetime import datetime
from db import connect_to_sqlite, close_sqlite_connection
from google.adk.tools import ToolContext

def raise_complaint(user_id: str, order_id: str, description: str , tool_context: ToolContext = None) -> str:
    """
    Raises a complaint and logs it both in the database and in the state.
    """

    created_at = datetime.now()
    timestamp_str = created_at.isoformat()
    complaint_ref = f"CPL-{created_at.strftime('%Y%m%d%H%M%S')}"
    status = "Pending"

    # 1. Log to DB
    conn = connect_to_sqlite()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO complaints (user_id, order_id, description, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, order_id, description, status, created_at.date().isoformat()))
        conn.commit()
    except Exception as e:
        return f"Failed to submit complaint: {str(e)}"
    finally:
        cursor.close()
        close_sqlite_connection(conn)

    complaint_entry = {
        "ref": complaint_ref,
        "order_id": order_id,
        "description": description,
        "status": status,
        "timestamp": timestamp_str
    }


    tool_context.state.setdefault("complaints", []).append(complaint_entry)
    tool_context.state.setdefault("interaction_history", []).append({
        "type": "complaint",
        "ref": complaint_ref,
        "order_id": order_id,
        "message": f"Complaint raised: {description}",
        "timestamp": timestamp_str
    })

    return (
        f"I'm really sorry to hear that. I've logged your complaint"
        f"{' for Order ID ' + str(order_id) if order_id else ''} with reference number {complaint_ref}. "
        f"Our support team will get back to you within 48 hours."
    )
