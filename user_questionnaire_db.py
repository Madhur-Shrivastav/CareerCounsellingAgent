import sqlite3
import uuid
import uuid
import json
import time


def add_questionnaire():
    conn = sqlite3.connect("customer_support.db")
    cursor = conn.cursor()

    doc = {
    "_id": {"$oid": str(uuid.uuid4())},
    "user_id": "1",
    "education_level": "10th",
    "responses": {
    "academic_strengths_subject": "🗺️ History / Political Science / Geography / Current Affairs",
    "stream_inclination": "🗳️ Exploring history, politics, society, and great leaders (Arts)",
    "academic_strengths_marks": "Math: 40–50%, Science: 80–90%, Social Science: 80–90%, English/Hindi: 40–50%, Computer IT: 80–90%",
    "future_profession_goal": "🏛️ Government Officer (IAS, IPS)",
    "natural_hobbies": "🎤 Speaking confidently, debating, or sharing opinions",
    "exciting_workplace": "🏛️ Government office setup",
    "free_time_activity": "🗳️ Watching or reading about history, political events, or current affairs",
    "career_influence": "👫 My friends or classmates",
    "activity_preference": "🗣️ Debates, quizzes, or political discussions",
    "youtube_channel_interest": "🗳️ Talking about history, politics, or current affairs",
    "flow_activity": "🗣️ Teaching, writing, or sharing thoughts with peers",
    "personality_type": "🤝 I enjoy helping, guiding, or supporting people",
    "career_reason_observed": "💸 For a high-paying or trending career",
    "confidence_stream_choice": "Somewhat confident, but need total clearity",
    "unsure_reason_multiple": "👪 My parents want something else, 💬 I need proper guidance or help",
    "self_statement": "🧘 I prefer calm focus. I enjoy working quietly and solving things in depth."
    },
    "timestamp": {"$date": {"$numberLong": str(int(time.time() * 1000))}}
    }

    cursor.execute("""
        INSERT INTO questionnaire (id, user_id, education_level, raw_responses, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        doc["_id"]["$oid"],
        doc["user_id"],
        doc["education_level"],
        json.dumps(doc["responses"]),
        int(doc["timestamp"]["$date"]["$numberLong"])
    ))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ New questionnaire added.")

def drop_and_recreate_questionnaire_table():
      
    try:
        conn = sqlite3.connect("customer_support.db")
        cursor = conn.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS questionnaire;")
            print("Successfully dropped 'questionnaire' table (if it existed).")
        except sqlite3.Error as e:
            print(f"Error dropping 'questionnaire' table: {e}")
            return 

        try:
            cursor.execute("""
                CREATE TABLE questionnaire (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,              -- UUID of the student
                    education_level TEXT NOT NULL,      -- e.g. "10th", "12th", "graduate"
                    raw_responses TEXT NOT NULL,        -- store JSON as TEXT (all responses together)
                    timestamp INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)
            print("Successfully created 'questionnaire' table with 'id' as TEXT and 'product_name' column.")
            conn.commit() 
        except sqlite3.Error as e:
            print(f"Error creating 'questionnaire' table: {e}")
            conn.rollback() 

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
            
drop_and_recreate_questionnaire_table()
add_questionnaire()