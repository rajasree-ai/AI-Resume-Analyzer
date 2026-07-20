"""
Supabase Client for ResumeAI
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    """Singleton Supabase client"""
    
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
        return cls._instance
    
    def get_client(self) -> Client:
        """Get or create Supabase client"""
        if self._client is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            
            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
            
            self._client = create_client(url, key)
            print("✅ Supabase client initialized")
        
        return self._client

# Singleton instance
supabase = SupabaseClient()

def get_supabase():
    """Get Supabase client instance"""
    return supabase.get_client()