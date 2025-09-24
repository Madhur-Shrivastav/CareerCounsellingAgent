import json
from google import genai
from .fetch_questionnaire import fetch_user_questionnaire
from .insert_profile import insert_user_profile
from ..sub_agent.RAG.similarity_search import search_documents
from ..schemas.profile import UserProfile

def generate_user_profile(user_id : str):
    questionnaire_responses = fetch_user_questionnaire(user_id=user_id)[0];
    query_text = json.dumps(questionnaire_responses, ensure_ascii=False)
    reference_documents = search_documents(query=query_text)
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=
        f"""
        You are an assistant that generates structured user profiles.
    
        **Input:**
        - User responses to a career questionnaire (provided in {questionnaire_responses}).
        - Refer the relevant documents fetched from semantic similarity search {reference_documents}.

        IMPORTANT: Your response must be MUST be valid JSON only, 

        DO NOT include any explanations or additional text outside the JSON response.
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": UserProfile,
        },
    )

    print("[User Profile]:", response.text)
    print("[Supabase Response]:",insert_user_profile(questionnaire_id=questionnaire_responses["id"],profile=response.text))
    return response.text