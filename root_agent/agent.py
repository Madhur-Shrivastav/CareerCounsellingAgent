import json
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional
# from db import connect_to_sqlite, close_sqlite_connection
from .functions.fetch_user import fetch_user_details
from .functions.fetch_questionnaire import fetch_user_questionnaire
from .functions.generate_profile import generate_user_profile

async def beforeagentcallback(callback_context: CallbackContext) -> Optional[types.Content]:
    user_id = callback_context.state.get("user_id", "eab7924b-8391-49b7-9a77-6a9abc665e9f")
    user_profile = callback_context.state.get("user_profile");
    if not user_profile:
        user_profile = json.loads(generate_user_profile(user_id=user_id))
    user_list = fetch_user_details(user_id=user_id)
    print(user_list)
    if user_list:
        user = user_list[0]
        callback_context.state["user_id"] = user["id"]
        callback_context.state["user_name"] = user["fullname"]
        callback_context.state["user_email"] = user["email"]
        callback_context.state["user_profile"] = user_profile
    
        questionnaire = fetch_user_questionnaire(user_id=user["id"])
        print(questionnaire)
        if questionnaire:
            callback_context.state["questionnaire_responses"] = questionnaire[0]

    return None



root_agent = LlmAgent(
    name="career_counsellor",
    model="gemini-2.0-flash",
    description="Career counselling agent that helps users explore their strengths, interests, and suitable career paths.",
    instruction="""
You are a career counsellor helping users explore their strengths, skills, and potential career paths based on their responses to a career questionnaire. 

**User Information:**
<user_info>
Name: {user_name}
Email: {user_email}
</user_info>

**User's questionnaire responses:**
<questionnaire>
{questionnaire_responses}
</questionnaire>

**User's profile:**
<user_profile>
{user_profile}
</user_profile>

**Your tasks:**
1. Analyze the user’s questionnaire and profile.
2. Suggest structured career paths with a match percentage.
3. Recommend actionable next steps to improve skills or explore careers further.
4. Highlight possible roadblocks and provide guidance to overcome them.
5. Provide an encouraging summary of the user’s profile.

**Behavior Guidelines:**
- Use empathy and clarity in all responses.
- Tailor suggestions based on user strengths, interests, and orientation.
""",
    sub_agents=[],
    tools=[],
    before_agent_callback=beforeagentcallback
)