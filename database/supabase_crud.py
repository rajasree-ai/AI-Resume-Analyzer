"""
Supabase CRUD Operations
"""

from .supabase_client import get_supabase
from datetime import datetime
import uuid

class SupabaseCRUD:
    """CRUD operations using Supabase"""
    
    def __init__(self, use_service_role=False):
        self.client = get_supabase(use_service_role)
        self.use_service_role = use_service_role
    
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
    
    def update_user(self, user_id, user_data):
        user_data['updated_at'] = datetime.now().isoformat()
        response = self.client.table('users').update(user_data).eq('id', user_id).execute()
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
    
    def update_resume(self, resume_id, resume_data):
        resume_data['updated_at'] = datetime.now().isoformat()
        response = self.client.table('resumes').update(resume_data).eq('id', resume_id).execute()
        return response.data[0] if response.data else None
    
    def delete_resume(self, resume_id):
        response = self.client.table('resumes').update({'is_deleted': True}).eq('id', resume_id).execute()
        return response.data[0] if response.data else None
    
    # ========== JOB OPERATIONS ==========
    
    def create_job(self, job_data):
        job_data['id'] = str(uuid.uuid4())
        job_data['created_at'] = datetime.now().isoformat()
        job_data['updated_at'] = datetime.now().isoformat()
        job_data['posted_date'] = datetime.now().isoformat()
        
        response = self.client.table('job_descriptions').insert(job_data).execute()
        return response.data[0] if response.data else None
    
    def get_job(self, job_id):
        response = self.client.table('job_descriptions').select('*').eq('id', job_id).execute()
        return response.data[0] if response.data else None
    
    def get_all_jobs(self, active_only=True):
        query = self.client.table('job_descriptions').select('*')
        if active_only:
            query = query.eq('is_active', True)
        response = query.order('created_at', desc=True).execute()
        return response.data
    
    # ========== ANALYSIS OPERATIONS ==========
    
    def create_analysis(self, analysis_data):
        analysis_data['id'] = str(uuid.uuid4())
        analysis_data['created_at'] = datetime.now().isoformat()
        analysis_data['updated_at'] = datetime.now().isoformat()
        
        response = self.client.table('analyses').insert(analysis_data).execute()
        return response.data[0] if response.data else None
    
    def get_analysis(self, analysis_id):
        response = self.client.table('analyses').select('*').eq('id', analysis_id).execute()
        return response.data[0] if response.data else None
    
    def get_resume_analyses(self, resume_id):
        response = self.client.table('analyses').select('*').eq('resume_id', resume_id).order('created_at', desc=True).execute()
        return response.data
    
    def get_user_analyses(self, user_id):
        response = self.client.table('analyses').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        return response.data
    
    def update_analysis(self, analysis_id, analysis_data):
        analysis_data['updated_at'] = datetime.now().isoformat()
        response = self.client.table('analyses').update(analysis_data).eq('id', analysis_id).execute()
        return response.data[0] if response.data else None

# Singleton instance
def get_crud(use_service_role=False):
    """Get CRUD instance"""
    return SupabaseCRUD(use_service_role=use_service_role)