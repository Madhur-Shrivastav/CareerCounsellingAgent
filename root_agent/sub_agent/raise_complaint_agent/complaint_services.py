from datetime import datetime
from typing import Optional
from google.adk.tools import ToolContext 
from db import connect_to_sqlite, close_sqlite_connection  

def raise_complaint(order_id: Optional[str] = None, 
                    description: str = "", 
                    product_name: Optional[str] = "", 
                    tool_context: ToolContext = None) -> str:

    request_date = datetime.now()
    complaint_ref = f"CPL-{request_date.strftime('%Y%m%d%H%M%S')}"
    complaint_type = "Product-Related"

    user_id = tool_context.state.get("user_id") if tool_context else None
    if not user_id:
        return "Unable to identify user. Please make sure you are logged in."

    conn = connect_to_sqlite()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO complaints (id, user_id, order_id, product_name, complaint_type, description, request_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            complaint_ref,
            user_id,
            order_id if order_id else None,
            product_name if product_name else "",
            complaint_type if product_name else "General",
            description,
            request_date.date().isoformat()
        ))
        conn.commit()

    except Exception as e:
        return f"Failed to submit complaint due to a database error: {str(e)}"

    finally:
        cursor.close()
        close_sqlite_connection(conn)

    return (
        f"📝 I've logged your complaint"
        f"{' for Order ID ' + order_id if order_id else ''} "
        f"with reference number **{complaint_ref}**. "
        f"Our support team will respond within 48 hours."
    )
