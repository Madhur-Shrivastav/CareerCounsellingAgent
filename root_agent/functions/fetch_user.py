from .get_supabase import get_supabase_client

def fetch_user_details(user_id):
    response = get_supabase_client().table('users').select('*').eq('id', user_id).execute()
    return response.data


user_id = 'eab7924b-8391-49b7-9a77-6a9abc665e9f'  
user_details = fetch_user_details(user_id)
print(user_details)
