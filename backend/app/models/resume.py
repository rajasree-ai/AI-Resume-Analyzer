"""
Resume Model
"""

from datetime import datetime

class Resume:
    """Resume model"""
    
    def __init__(self, id=None, user_id=None, filename=None, file_path=None,
                 file_size=0, file_type='pdf', original_text=None, parsed_data=None,
                 skills=None, education=None, experience=None, contact=None,
                 is_processed=False, is_deleted=False, upload_date=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.filename = filename
        self.file_path = file_path
        self.file_size = file_size
        self.file_type = file_type
        self.original_text = original_text
        self.parsed_data = parsed_data
        self.skills = skills or []
        self.education = education or []
        self.experience = experience or []
        self.contact = contact or {}
        self.is_processed = is_processed
        self.is_deleted = is_deleted
        self.upload_date = upload_date or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.analysis_results = []
    
    def to_dict(self):
        """Convert resume to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'is_processed': self.is_processed,
            'skills': self.skills or [],
            'education': self.education or [],
            'experience': self.experience or [],
            'contact': self.contact or {},
            'word_count': len(self.original_text.split()) if self.original_text else 0
        }


class JobDescription:
    """Job Description model"""
    
    def __init__(self, id=None, title=None, company=None, location=None,
                 job_type=None, experience_level=None, description=None,
                 responsibilities=None, requirements=None, nice_to_have=None,
                 benefits=None, required_skills=None, preferred_skills=None,
                 education_required=None, experience_required=0,
                 salary_min=None, salary_max=None, currency='USD',
                 is_active=True, created_at=None, updated_at=None, posted_date=None):
        self.id = id
        self.title = title
        self.company = company
        self.location = location
        self.job_type = job_type
        self.experience_level = experience_level
        self.description = description
        self.responsibilities = responsibilities or []
        self.requirements = requirements or []
        self.nice_to_have = nice_to_have or []
        self.benefits = benefits or []
        self.required_skills = required_skills or []
        self.preferred_skills = preferred_skills or []
        self.education_required = education_required or []
        self.experience_required = experience_required
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.posted_date = posted_date or datetime.utcnow()
        self.analyses = []
    
    def to_dict(self):
        """Convert job description to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'job_type': self.job_type,
            'experience_level': self.experience_level,
            'description': self.description,
            'responsibilities': self.responsibilities or [],
            'requirements': self.requirements or [],
            'nice_to_have': self.nice_to_have or [],
            'benefits': self.benefits or [],
            'required_skills': self.required_skills or [],
            'preferred_skills': self.preferred_skills or [],
            'education_required': self.education_required or [],
            'experience_required': self.experience_required,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'currency': self.currency,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'posted_date': self.posted_date.isoformat() if self.posted_date else None
        }