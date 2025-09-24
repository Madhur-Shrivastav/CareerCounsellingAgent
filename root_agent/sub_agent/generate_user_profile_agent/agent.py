from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from ..RAG.similarity_search import search_documents
from ...schemas.profile import UserProfile
from ...functions.insert_profile import insert_user_profile
from google import genai
import json
from typing import Optional
from google.genai import types

async def beforeagentcallback(callback_context: CallbackContext) -> Optional[types.Content]:
    questionnaire_responses = callback_context.state['questionnaire_responses']
    query_text = " ".join([f"{k}: {v}" for k, v in questionnaire_responses.items()])
    reference_documents = search_documents(query=query_text)
    callback_context.state['docs'] = reference_documents

def generate_user_profile():
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=
        f"""
        You are an assistant that generates structured user profiles.
    
        **Input:**
        - User responses to a career questionnaire (provided in {questionnaire_responses}).
        - Refer the relevant documents fetched from semantic similarity search {reference_documents}.

        IMPORTANT: Your response must be MUST be valid JSON only, matching this structure:
        {
            "profile_summary": "Brief summary of the student's overall traits and inclinations.",
            "identified_keywords": ["Keyword1", "Keyword2", "Keyword3", "Keyword4", "Keyword5"],
            "primary_orientation": "Analytical",
            "orientation_confidence": 0-100,
            "analytical": 0-100,
            "creative": 0-100,
            "social": 0-100,
            "practical": 0-100,
            "investigative": 0-100,
            "top_strength": "Ex:Problem-Solving",
            "learning_style": "Visual",
            "potential_career_paths": [
                {"path": "Career Title 1", "match_percentage": 0-100},
                {"path": "Career Title 2", "match_percentage": 0-100},
                {"path": "Career Title 3", "match_percentage": 0-100}
            ],
            "recommended_next_steps": [
                "Action-oriented and practical step 1",
                "Action-oriented and practical step 2"
            ],
            "confidence_indicators": {
                "decision_making": "High",
                "self_awareness": "Medium",
                "exploration_readiness": "High"
            },
            "interest_distribution": {
                "STEM": 0-100,
                "Arts_Humanities": 0-100,
                "Business_Commerce": 0-100,
                "Social_Services": 0-100
            },
            "welcome_statement": "A warm and motivational message acknowledging the student's effort.",
            "your_natural_inclination": "Summary of domains or tasks the student naturally enjoys.",
            "possible_roadblocks": [
                "Roadblock 1 with soft advice",
                "Roadblock 2 with soft advice"
            ],
            "remarks": "Mentor-like advice with a positive tone.",
            "profile_in_a_gist": {
                "subjects_good_at": ["Subject1", "Subject2"],
                "natural_calling": "Summary of natural interests or inclinations",
                "inclined_to_pursue": ["Career Path 1", "Career Path 2"],
                "roadblocks": ["Main challenge(s) faced"],
                "encouragement": "Positive and motivating advice"
            },
            "final_note": "A strong concluding sentence – inspiring and reassuring."
        }

        DO NOT include any explanations or additional text outside the JSON response.
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": UserProfile,
        },
    )

    print("[Debug] Raw model response:", response.text)
    insert_user_profile(response.text)

generate_user_profile_agent = Agent(
    name="generate_user_profile_agent",
    description="Generates a structured user profile JSON output on questionnaire responses and similarity search documents.",
    output_schema=UserProfile,
    output_key="user_profile",
    instruction=
    f""" 
    You are an assistant that generates structured user profiles.
    IMPORTANT:To generate user profile call the functional tool:'generate_user_profile'
    """,
    tools=[generate_user_profile],
)
