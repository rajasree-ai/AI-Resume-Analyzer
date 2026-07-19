from typing import Dict, List, Any, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class JobMatcher:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
        
    def extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract key requirements from job description"""
        requirements = {
            'skills': [],
            'education': [],
            'experience': [],
            'soft_skills': [],
            'technical_skills': []
        }
        
        # Extract skills mentioned in JD
        skill_patterns = [
            r'(?:skills?|technologies?|tools?|languages?|frameworks?):?\s*([^\n.]+)',
            r'(?:required|minimum|preferred)\s+(?:skills?|qualifications?):?\s*([^\n.]+)',
            r'(?:proficient|experienced|knowledgeable)\s+in\s+([^\n.]+)'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            for match in matches:
                skills = re.split(r'[,;|&]|\band\b', match)
                requirements['skills'].extend([s.strip().lower() for s in skills if len(s.strip()) > 2])
        
        # Extract education requirements
        edu_patterns = [
            r'(?:bachelor|master|phd|degree|education).*?(?:in|of)\s+([^\n.]+)',
            r'(?:minimum|required)\s+(?:education|qualification).*?([^\n.]+)'
        ]
        
        for pattern in edu_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            requirements['education'].extend([m.strip() for m in matches])
        
        # Extract experience requirements
        exp_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience)',
            r'experience\s*(?:in|with)\s*([^\n.]+)'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            requirements['experience'].extend([m.strip() for m in matches])
        
        return requirements
    
    def calculate_resume_job_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate semantic similarity between resume and job description"""
        # Combine sections for better representation
        resume_embedding = self.model.encode([resume_text[:1000]])  # Limit for performance
        job_embedding = self.model.encode([job_text[:1000]])
        
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        return similarity * 100
    
    def match_experience_level(self, resume: Dict, job_requirements: Dict) -> int:
        """Match experience level between resume and job requirements"""
        # Extract years of experience from resume
        resume_years = 0
        for exp in resume.get('experience', []):
            years = re.search(r'(\d+)\s*(?:years?|yrs?)', exp.get('text', ''), re.IGNORECASE)
            if years:
                resume_years += int(years.group(1))
        
        # Extract required years from job
        required_years = 0
        for req in job_requirements.get('experience', []):
            years = re.search(r'(\d+)', req)
            if years:
                required_years = max(required_years, int(years.group(1)))
        
        if resume_years >= required_years:
            return 100
        elif resume_years >= required_years * 0.7:
            return 70
        else:
            return int((resume_years / required_years) * 100) if required_years > 0 else 100
    
    def generate_compatibility_report(self, resume_data: Dict, job_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive compatibility report"""
        resume_text = resume_data.get('raw_text', '')
        job_text = job_data.get('description', '')
        
        # Calculate similarity scores
        semantic_score = self.calculate_resume_job_similarity(resume_text, job_text)
        
        # Extract job requirements
        job_requirements = self.extract_job_requirements(job_text)
        
        # Match skills
        resume_skills = resume_data.get('skills', [])
        job_skills = job_requirements.get('skills', [])
        
        skill_match_result = self.match_skills(resume_skills, job_skills)
        
        # Calculate experience match
        experience_match = self.match_experience_level(resume_data, job_requirements)
        
        # Calculate overall compatibility
        weights = {
            'skills': 0.5,
            'semantic': 0.3,
            'experience': 0.2
        }
        
        overall_score = (
            weights['skills'] * skill_match_result['match_rate'] * 100 +
            weights['semantic'] * semantic_score +
            weights['experience'] * experience_match
        )
        
        return {
            'overall_score': overall_score,
            'skill_match_score': skill_match_result['match_rate'] * 100,
            'semantic_similarity': semantic_score,
            'experience_match': experience_match,
            'matching_skills': skill_match_result['matching_skills'],
            'missing_skills': skill_match_result['missing_skills'],
            'exact_matches': skill_match_result['exact_matches'],
            'semantic_matches': skill_match_result['semantic_matches'],
            'job_requirements': job_requirements,
            'recommendations': {
                'skills_to_learn': skill_match_result['missing_skills'][:10],
                'priority_skills': self._get_priority_skills(skill_match_result['missing_skills'])
            }
        }
    
    def _get_priority_skills(self, missing_skills: List[str]) -> List[str]:
        """Get priority skills from missing list"""
        # This would typically prioritize based on job market demand
        priority_keywords = ['python', 'java', 'sql', 'react', 'aws', 'docker', 'kubernetes']
        priority = []
        
        for skill in missing_skills:
            if skill in priority_keywords:
                priority.append(skill)
        
        return priority[:5]
    
    def match_skills(self, resume_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
        """Match skills between resume and job"""
        # Same implementation as in SkillAnalyzer
        from .skill_analyzer import SkillAnalyzer
        analyzer = SkillAnalyzer()
        return analyzer.match_skills(resume_skills, job_skills)