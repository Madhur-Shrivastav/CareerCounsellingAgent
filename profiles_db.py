import sqlite3
import uuid
import uuid
import json
import time


profile_data = {
    "questionnaire_id": "03629a4e-efaa-40b7-9b24-e129a7a24b27",  
    "profile_summary": "A focused and socially driven learner with strong interests in history, politics, and social sciences, aiming for a government career with a calm, thoughtful approach.",
    "identified_keywords": ["Government Service","Debating","Social Science","Leadership","Public Speaking"],
    "primary_orientation": "Social",
    "orientation_confidence": 85,
    "analytical": 70,
    "creative": 55,
    "social": 90,
    "practical": 60,
    "investigative": 75,
    "top_strength": "Effective Communication",
    "learning_style": "Reading",
    "potential_career_paths": [
        {"path":"IAS Officer","match_percentage":90},
        {"path":"Political Analyst","match_percentage":75},
        {"path":"Public Relations Specialist","match_percentage":65}
    ],
    "recommended_next_steps": [
        "Engage in more debates and quizzes to sharpen public speaking skills",
        "Seek mentorship and guidance on government service exam preparation"
    ],
    "confidence_indicators": {"decision_making":"Medium","self_awareness":"Medium","exploration_readiness":"High"},
    "interest_distribution": {"STEM":40,"Arts_Humanities":85,"Business_Commerce":30,"Social_Services":80},
    "welcome_statement": "Great job exploring your interests and strengths! Keep up your curiosity and enthusiasm for learning.",
    "your_natural_inclination": "Drawn to history, politics, and social studies with a passion for understanding society and leadership.",
    "potential_career_options": ["Government Officer (IAS/IPS)","Political Analyst","Public Relations or Social Advocacy"],
    "your_strengths_and_qualities": [
        "Strong communication and debating skills",
        "Calm focus and deep problem-solving ability",
        "Supportive and helpful nature"
    ],
    "possible_roadblocks": [
        "Uncertainty due to parental expectations",
        "Need for clearer guidance on career paths"
    ],
    "remarks": "Stay curious and proactive in exploring your interests.",
    "profile_in_a_gist": {
        "subjects_good_at":["Social Science","Science","Computer IT"],
        "natural_calling":"Exploring history, politics, and societal issues through discussion and debate",
        "inclined_to_pursue":["Government service","Political analysis","Public speaking roles"],
        "roadblocks":["Parental pressure","Need for more career clarity"],
        "encouragement":"You're not expected to have all the answers today. Stay curious and keep learning!"
    },
    "final_note": "You don’t need to have all the answers right now — stay curious, keep exploring, and trust the learning process."
}

def add_profile(profile):
    conn = sqlite3.connect("customer_support.db")
    cursor = conn.cursor()
    profile_id = str(uuid.uuid4())
    
    cursor.execute("""
        INSERT INTO profiles (
            id,
            questionnaire_id,
            profile_summary,
            identified_keywords,
            primary_orientation,
            orientation_confidence,
            analytical,
            creative,
            social,
            practical,
            investigative,
            top_strength,
            learning_style,
            potential_career_paths,
            recommended_next_steps,
            confidence_indicators,
            interest_distribution,
            welcome_statement,
            your_natural_inclination,
            potential_career_options,
            your_strengths_and_qualities,
            possible_roadblocks,
            remarks,
            profile_in_a_gist,
            final_note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile_id,
        profile["questionnaire_id"],
        profile.get("profile_summary"),
        json.dumps(profile.get("identified_keywords", [])),
        profile.get("primary_orientation"),
        profile.get("orientation_confidence"),
        profile.get("analytical"),
        profile.get("creative"),
        profile.get("social"),
        profile.get("practical"),
        profile.get("investigative"),
        profile.get("top_strength"),
        profile.get("learning_style"),
        json.dumps(profile.get("potential_career_paths", [])),
        json.dumps(profile.get("recommended_next_steps", [])),
        json.dumps(profile.get("confidence_indicators", {})),
        json.dumps(profile.get("interest_distribution", {})),
        profile.get("welcome_statement"),
        profile.get("your_natural_inclination"),
        json.dumps(profile.get("potential_career_options", [])),
        json.dumps(profile.get("your_strengths_and_qualities", [])),
        json.dumps(profile.get("possible_roadblocks", [])),
        profile.get("remarks"),
        json.dumps(profile.get("profile_in_a_gist", {})),
        profile.get("final_note")
    ))

    conn.commit()
    conn.close()
    print(f"✅ Profile added with ID: {profile_id}")

def drop_and_recreate_profiles_table():
      
    try:
        conn = sqlite3.connect("customer_support.db")
        cursor = conn.cursor()
        try:
            cursor.execute("DROP TABLE IF EXISTS profiles;")
            print("Successfully dropped 'profiles' table (if it existed).")
        except sqlite3.Error as e:
            print(f"Error dropping 'profiles' table: {e}")
            return 

        try:
            cursor.execute("""
                CREATE TABLE profiles (
                    id TEXT PRIMARY KEY,
                    questionnaire_id INTEGER NOT NULL,       -- FK to user_responses.id
                    profile_summary TEXT,
                    identified_keywords TEXT,           -- store JSON list as TEXT
                    primary_orientation TEXT,
                    orientation_confidence INTEGER,
                    
                    analytical INTEGER,
                    creative INTEGER,
                    social INTEGER,
                    practical INTEGER,
                    investigative INTEGER,

                    top_strength TEXT,
                    learning_style TEXT,

                    potential_career_paths TEXT,        -- store JSON array {path, match_percentage}
                    recommended_next_steps TEXT,        -- JSON array
                    confidence_indicators TEXT,         -- JSON object
                    interest_distribution TEXT,         -- JSON object
                    welcome_statement TEXT,
                    your_natural_inclination TEXT,
                    potential_career_options TEXT,      -- JSON array
                    your_strengths_and_qualities TEXT,  -- JSON array
                    possible_roadblocks TEXT,           -- JSON array
                    remarks TEXT,
                    profile_in_a_gist TEXT,             -- JSON object
                    final_note TEXT,

                    FOREIGN KEY (questionnaire_id) REFERENCES questionnaire(id)
                );
            """)
            print("Successfully created 'profiles' table with 'id' as TEXT.")
            conn.commit() 
        except sqlite3.Error as e:
            print(f"Error creating 'profiles' table: {e}")
            conn.rollback() 

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
            
drop_and_recreate_profiles_table()
add_profile(profile_data)