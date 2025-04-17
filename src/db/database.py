from datetime import datetime
import os
from supabase import create_client, Client
from fastapi import Request

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
#supabase: Client = create_client(url, key)
supabase = create_client(url, key)

# Mock user ID for testing purposes
def get_mock_user_id(request: Request):
    # For testing, we are using a hardcoded user ID
    return "mock_user_id_123"  # Replace with any string to simulate a user ID

# Save a new question to Supabase
def save_question(user_id, question, interpretation, datetime_data, location_data):
    data = {
        "user_id": user_id,
        "question": question,
        "interpretation": interpretation,
        "datetime": str(datetime_data),
        "location": str(location_data),
        "created_at": datetime.now().isoformat()
    }
    supabase.table("user_questions").insert(data).execute()


# Get the last N questions for a user
def get_last_n_questions(user_id, n=3):
    response = supabase.table("user_questions") \
        .select("question, interpretation") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .limit(n) \
        .execute()

    return response.data