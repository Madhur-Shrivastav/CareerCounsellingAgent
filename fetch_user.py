import sqlite3
import json

def get_full_user_data(user_id):
    conn = sqlite3.connect("customer_support.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get user info
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    if not user_row:
        print(f"No user found with id: {user_id}")
        return None
    user_dict = {key: user_row[key] for key in user_row.keys()}

    # Get questionnaire
    cursor.execute("""
        SELECT * FROM questionnaire WHERE user_id = ?
    """, (user_id,))
    q_row = cursor.fetchone()
    if q_row:
        user_dict['questionnaire'] = {key: q_row[key] for key in q_row.keys()}
    else:
        user_dict['questionnaire'] = None

    if q_row:
        q_id = q_row['id']
        
        cursor.execute("""
            SELECT * FROM profiles WHERE questionnaire_id = ?
        """, (q_id,))
        p_row = cursor.fetchone()
        print(p_row)
        if p_row:
            user_dict['profile'] = {key: p_row[key] for key in p_row.keys()}
        else:
            user_dict['profile'] = None
    else:
        user_dict['profile'] = None

    cursor.close()
    conn.close()

    # Convert to JSON string
    full_json = json.dumps(user_dict, ensure_ascii=False, indent=2)
    return full_json

full_user_json = get_full_user_data("1")
print(full_user_json)
