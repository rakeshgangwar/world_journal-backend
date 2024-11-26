import os

import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
API_KEY = os.getenv("SUPABASE_API_KEY")

def fetch_feeds_by_category(category_id: int = None):
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
    }

    response = requests.get(SUPABASE_URL + f"feeds?categoryId=eq.{category_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def fetch_category(category_id: int):
    headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
    }

    response = requests.get(SUPABASE_URL + f"feed_categories?categoryId=eq.{category_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None