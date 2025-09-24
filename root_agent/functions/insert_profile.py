from supabase import create_client, Client
from typing import Dict
import json
from .get_supabase import get_supabase_client

def insert_user_profile(questionnaire_id:str, profile:Dict=None):
    user_profile = json.loads(profile)
    response = (
        get_supabase_client().table("profiles")
        .insert({ "questionnaire_id":questionnaire_id,"user_profile": user_profile })
        .execute()
        )
    return response