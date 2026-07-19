"""
Helper functions
"""

import re
import json
from datetime import datetime

class Helpers:
    """Utility helper functions"""
    
    @staticmethod
    def extract_skills(text: str) -> list:
        """Extract skills from text"""
        skills = []
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'html', 'css', 'sql', 'mongodb', 'postgresql', 'mysql', 'docker',
            'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'tensorflow',
            'pytorch', 'scikit-learn', 'pandas', 'numpy', 'django', 'flask'
        ]
        text_lower = text.lower()
        for skill in common_skills:
            if skill in text_lower:
                skills.append(skill)
        return skills
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password strength"""
        return len(password) >= 6