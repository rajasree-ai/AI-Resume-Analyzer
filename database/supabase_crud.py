"""
Supabase CRUD Operations
"""

from .supabase_client import get_supabase
from datetime import datetime
import uuid

class SupabaseCRUD:
    """CRUD operations using Supabase"""
    
    def __init__(self):
        self.client = get_supabase()
    
    # ========== USER OPERATIONS ==========
    
    def create_user(self, user_data):
        user_data['id'] = str(uuid.uuid4())
        user_data['created_at'] = datetime.now().isoformat()
        user_data['updated_at'] = datetime.now().isoformat()
        
        response = self.client.table('users').insert(user_data).execute()
        return response.data[0] if response.data else None
    
    def get_user(self, user_id):
        response = self.client.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None
    
    def get_user_by_email(self, email):
        response = self.client.table('users').select('*').eq('email', email).execute()
        return response.data[0] if response.data else None
    
    # ========== RESUME OPERATIONS ==========
    
    def create_resume(self, resume_data):
        resume_data['id'] = str(uuid.uuid4())
        resume_data['upload_date'] = datetime.now().isoformat()
        resume_data['updated_at'] = datetime.now().isoformat()
        
        response = self.client.table('resumes').insert(resume_data).execute()
        return response.data[0] if response.data else None
    
    def get_resume(self, resume_id):
        response = self.client.table('resumes').select('*').eq('id', resume_id).execute()
        return response.data[0] if response.data else None
    
    def get_user_resumes(self, user_id):
        response = self.client.table('resumes').select('*').eq('user_id', user_id).order('upload_date', desc=True).execute()
        return response.data
    
    # ========== ANALYSIS OPERATIONS ==========
    
    def create_analysis(self, analysis_data):
        analysis_data['id'] = str(uuid.uuid4())
        analysis_data['created_at'] = datetime.now().isoformat()
        analysis_data['updated_at'] = datetime.now().isoformat()
        
        response = self.client.table('analyses').insert(analysis_data).execute()
        return response.data[0] if response.data else None

# Singleton instance
crud = SupabaseCRUD()

def get_crud():
    """Get CRUD instance"""
    return crud