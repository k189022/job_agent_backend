from dotenv import load_dotenv
from fastapi import Header, HTTPException

import os

from supabase import Client, create_client

load_dotenv()

NEXT_PUBLIC_SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
NEXT_PUBLIC_SUPABASE_ANON_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")


# Initialize Supabase client (ensure these values are set properly)
supabase_url = NEXT_PUBLIC_SUPABASE_URL
supabase_key = NEXT_PUBLIC_SUPABASE_ANON_KEY
supabase: Client = create_client(supabase_url, supabase_key)


def get_supabase_user(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization scheme.")
    
    token = authorization.split(" ")[1]
    user_id = None
    try:
        response = supabase.auth.get_user(token)
        if response.user:
            user_id = response.user.id
        else:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")
    return user_id

# result = get_supabase_user(hardcode_token)

# print(result)