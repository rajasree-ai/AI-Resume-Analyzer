"""
User Model with Authentication
"""

from datetime import datetime, timedelta
import jwt
import os
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

class User:
    """User model"""
    
    def __init__(self, id=None, username=None, email=None, password_hash=None, 
                 full_name=None, bio=None, is_active=True, is_admin=False,
                 created_at=None, updated_at=None, last_login=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.bio = bio
        self.is_active = is_active
        self.is_admin = is_admin
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.last_login = last_login
        self.resumes = []
        self.analyses = []
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        return False
    
    def generate_auth_token(self, expires_in=7):
        """Generate JWT token for authentication"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'username': self.username,
            'is_admin': self.is_admin,
            'exp': datetime.utcnow() + timedelta(days=expires_in)
        }
        return jwt.encode(payload, os.environ.get('SECRET_KEY', 'dev-key'), algorithm='HS256')
    
    @staticmethod
    def verify_auth_token(token):
        """Verify JWT token and return user data"""
        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY', 'dev-key'), algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def to_dict(self, include_token=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'bio': self.bio,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'resume_count': len(self.resumes) if self.resumes else 0,
            'analysis_count': len(self.analyses) if self.analyses else 0
        }
        
        if include_token:
            data['token'] = self.generate_auth_token()
        
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'