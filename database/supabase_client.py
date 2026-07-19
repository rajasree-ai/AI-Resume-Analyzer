"""
Supabase Client - Single source of truth
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    """Singleton Supabase client"""
    
    _instance = None
    _client = None
    _service_client = None
    
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
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment")
            
            self._client = create_client(url, key)
            print("✅ Supabase client initialized")
        
        return self._client
    
    def get_service_client(self) -> Client:
        """Get service role client (bypasses RLS)"""
        if self._service_client is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
            
            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
            
            self._service_client = create_client(url, key)
            print("✅ Supabase service client initialized")
        
        return self._service_client

# Singleton instance
supabase = SupabaseClient()

def get_supabase(use_service_role=False):
    """Get Supabase client"""
    if use_service_role:
        return supabase.get_service_client()
    return supabase.get_client()

# Alias for backward compatibility
get_supabase_client = get_supabase