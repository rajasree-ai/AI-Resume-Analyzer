"""
Analysis Model
"""

from datetime import datetime

class Analysis:
    """Analysis model"""
    
    def __init__(self, id=None, user_id=None, resume_id=None, job_id=None,
                 compatibility_score=0, ats_score=0, skill_match_score=0,
                 experience_match_score=0, education_match_score=0,
                 keyword_match_score=0, matching_skills=None, missing_skills=None,
                 extra_skills=None, partial_matches=None, skill_gap_analysis=None,
                 recommendations=None, improvements=None, feedback_rating=None,
                 feedback_comment=None, analysis_duration=0, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.resume_id = resume_id
        self.job_id = job_id
        self.compatibility_score = compatibility_score
        self.ats_score = ats_score
        self.skill_match_score = skill_match_score
        self.experience_match_score = experience_match_score
        self.education_match_score = education_match_score
        self.keyword_match_score = keyword_match_score
        self.matching_skills = matching_skills or []
        self.missing_skills = missing_skills or []
        self.extra_skills = extra_skills or []
        self.partial_matches = partial_matches or []
        self.skill_gap_analysis = skill_gap_analysis or {}
        self.recommendations = recommendations or {}
        self.improvements = improvements or {}
        self.feedback_rating = feedback_rating
        self.feedback_comment = feedback_comment
        self.analysis_duration = analysis_duration
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert analysis to dictionary"""
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'job_id': self.job_id,
            'compatibility_score': self.compatibility_score,
            'ats_score': self.ats_score,
            'skill_match_score': self.skill_match_score,
            'experience_match_score': self.experience_match_score,
            'education_match_score': self.education_match_score,
            'keyword_match_score': self.keyword_match_score,
            'matching_skills': self.matching_skills or [],
            'missing_skills': self.missing_skills or [],
            'extra_skills': self.extra_skills or [],
            'partial_matches': self.partial_matches or [],
            'skill_gap_analysis': self.skill_gap_analysis or {},
            'recommendations': self.recommendations or {},
            'improvements': self.improvements or {},
            'feedback_rating': self.feedback_rating,
            'feedback_comment': self.feedback_comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }