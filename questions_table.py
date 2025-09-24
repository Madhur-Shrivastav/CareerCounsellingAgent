import sqlite3
import uuid
import sqlite3
import uuid
import json

def add_question():
    conn = sqlite3.connect("customer_support.db")
    cursor = conn.cursor()

    question_data = (
        str(uuid.uuid4()),  
        "10th",  # education_level
        "academic_strengths_subject",  # name
        "Q1.",  # title
        "Which subjects do you feel most confident in, without needing much help?",  # prompt
        "multi",  # type
        json.dumps([
            "📐 Mathematics",
            "⚗️ Physics / Chemistry",
            "🧬 Biology / Environmental Science",
            "🗺️ History / Political Science / Geography / Current Affairs",
            "💼 Business Studies / Accounts / Economics",
            "💻 Computers / Tech / Coding"
        ]),  # options as JSON string
        None,   # grouped_options
        json.dumps({}),  # depends_on
        1,      # is_required (1 = True)
        1       # q_order
    )

    cursor.execute("""
        INSERT INTO questions (
            id, education_level, name, title, prompt, type,
            options, grouped_options, depends_on, is_required, q_order
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, question_data)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ New question added.")


import sqlite3

def drop_and_recreate_questions_table():
    try:
        conn = sqlite3.connect("customer_support.db")
        cursor = conn.cursor()
        
        # Drop table if it exists
        cursor.execute("DROP TABLE IF EXISTS questions;")
        print("Successfully dropped 'questions' table (if it existed).")

        # Recreate table
        cursor.execute("""
            CREATE TABLE questions (
                id TEXT PRIMARY KEY,
                education_level TEXT NOT NULL,     -- e.g. "10th"
                name TEXT NOT NULL,                -- e.g. "academic_strengths_subject"
                title TEXT NOT NULL,               -- e.g. "Q1."
                prompt TEXT NOT NULL,              -- the question text
                type TEXT NOT NULL,                -- type of question (multi, single, text, etc.)
                options TEXT,                      -- store JSON as TEXT in SQLite
                grouped_options TEXT,              -- can be NULL if unused
                depends_on TEXT,                   -- store JSON as TEXT
                is_required INTEGER NOT NULL DEFAULT 1,  -- 1 = true, 0 = false
                q_order INTEGER NOT NULL           -- order of the question
            );
        """)
        print("Successfully created 'questions' table.")
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

drop_and_recreate_questions_table()

add_question()


