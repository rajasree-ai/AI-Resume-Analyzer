"""
Analysis Service - Simplified version without sklearn
"""

import re
import json
from typing import Dict, List, Any
from datetime import datetime

class AnalysisService:
    """Service for analyzing resumes against job descriptions"""
    
    def __init__(self):
        self.skill_keywords = self._load_skill_keywords()
    
    def _load_skill_keywords(self) -> Dict[str, List[str]]:
        """Load skill keywords database"""
        try:
            with open('backend/data/skills_database.json', 'r') as f:
                return json.load(f)
        except:
            return {
                'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'typescript'],
                'web_development': ['react', 'angular', 'vue', 'node.js', 'html', 'css', 'django', 'flask'],
                'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras'],
                'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
                'soft_skills': ['communication', 'leadership', 'teamwork', 'problem-solving']
            }
    
    def analyze_resume_vs_job(self, resume_data: Dict, job_description: str) -> Dict[str, Any]:
        """Complete analysis of resume against job description"""
        
        job_requirements = self._extract_job_requirements(job_description)
        resume_skills = resume_data.get('skills', [])
        
        skill_analysis = self._analyze_skills(resume_skills, job_requirements.get('skills', []))
        
        keyword_match = self._calculate_keyword_match(
            resume_data.get('raw_text', ''),
            job_description
        )
        
        experience_match = self._calculate_experience_match(
            resume_data.get('experience', []),
            job_requirements.get('experience', [])
        )
        
        education_match = self._calculate_education_match(
            resume_data.get('education', []),
            job_requirements.get('education', [])
        )
        
        overall_score = self._calculate_overall_score({
            'skills': skill_analysis['match_score'],
            'keyword': keyword_match,
            'experience': experience_match,
            'education': education_match
        })
        
        recommendations = self._generate_recommendations(
            skill_analysis['missing_skills'],
            job_requirements
        )
        
        return {
            'overall_score': overall_score,
            'skill_analysis': skill_analysis,
            'keyword_match': keyword_match,
            'experience_match': experience_match,
            'education_match': education_match,
            'job_requirements': job_requirements,
            'recommendations': recommendations,
            'matching_skills': skill_analysis['matching_skills'],
            'missing_skills': skill_analysis['missing_skills'],
            'skill_gap_analysis': self._generate_gap_analysis(skill_analysis)
        }
    
    def _extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract requirements from job description"""
        requirements = {
            'skills': [],
            'education': [],
            'experience': [],
            'soft_skills': [],
            'technical_skills': []
        }
        
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
        
        requirements['skills'] = list(set(requirements['skills']))
        
        edu_patterns = [
            r'(?:bachelor|master|phd|degree|education).*?(?:in|of)\s+([^\n.]+)',
            r'(?:minimum|required)\s+(?:education|qualification).*?([^\n.]+)'
        ]
        
        for pattern in edu_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            requirements['education'].extend([m.strip() for m in matches])
        
        exp_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience)',
            r'experience\s*(?:in|with)\s*([^\n.]+)'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            requirements['experience'].extend([m.strip() for m in matches])
        
        return requirements
    
    def _analyze_skills(self, resume_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
        """Analyze skill match between resume and job"""
        resume_skills_lower = [s.lower().strip() for s in resume_skills]
        job_skills_lower = [s.lower().strip() for s in job_skills]
        
        exact_matches = set(resume_skills_lower) & set(job_skills_lower)
        
        partial_matches = []
        for resume_skill in resume_skills_lower:
            for job_skill in job_skills_lower:
                if (resume_skill in job_skill or job_skill in resume_skill) and resume_skill not in exact_matches:
                    partial_matches.append({
                        'resume_skill': resume_skill,
                        'job_skill': job_skill,
                        'match_type': 'partial'
                    })
        
        all_matching = set(exact_matches)
        for match in partial_matches:
            all_matching.add(match['job_skill'])
        
        missing_skills = set(job_skills_lower) - all_matching
        
        total_required = len(job_skills_lower) or 1
        match_score = (len(all_matching) / total_required) * 100
        
        return {
            'matching_skills': list(exact_matches),
            'partial_matches': partial_matches,
            'missing_skills': list(missing_skills),
            'match_score': min(100, match_score),
            'total_resume_skills': len(resume_skills),
            'total_job_skills': len(job_skills)
        }
    
    def _calculate_keyword_match(self, resume_text: str, job_text: str) -> float:
        """Calculate keyword similarity (simple version)"""
        resume_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text.lower()))
        job_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_text.lower()))
        
        if not job_words:
            return 50.0
        
        common = resume_words & job_words
        score = (len(common) / len(job_words)) * 100
        return min(100, score)
    
    def _calculate_experience_match(self, resume_experience: List, job_experience: List) -> float:
        """Calculate experience match"""
        resume_years = 0
        for exp in resume_experience:
            years = re.search(r'(\d+)\s*(?:years?|yrs?)', exp.get('text', ''), re.IGNORECASE)
            if years:
                resume_years += int(years.group(1))
        
        required_years = 0
        for req in job_experience:
            years = re.search(r'(\d+)', req)
            if years:
                required_years = max(required_years, int(years.group(1)))
        
        if required_years == 0:
            return 100.0
        
        if resume_years >= required_years:
            return 100.0
        elif resume_years >= required_years * 0.7:
            return 70.0
        else:
            return (resume_years / required_years) * 100
    
    def _calculate_education_match(self, resume_education: List, job_education: List) -> float:
        """Calculate education match"""
        if not job_education:
            return 100.0
        if not resume_education:
            return 0.0
        
        education_levels = {
            'phd': 4,
            'master': 3,
            'bachelor': 2,
            'associate': 1,
            'high school': 0
        }
        
        resume_level = 0
        for edu in resume_education:
            edu_text = edu.get('text', '').lower()
            for level, value in education_levels.items():
                if level in edu_text:
                    resume_level = max(resume_level, value)
        
        job_level = 0
        for edu in job_education:
            edu_text = edu.lower()
            for level, value in education_levels.items():
                if level in edu_text:
                    job_level = max(job_level, value)
        
        if job_level == 0:
            return 100.0
        
        match_percentage = (resume_level / job_level) * 100
        return min(100, match_percentage)
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate overall compatibility score with weights"""
        weights = {
            'skills': 0.5,
            'keyword': 0.2,
            'experience': 0.2,
            'education': 0.1
        }
        
        total_score = 0
        for key, weight in weights.items():
            if key in scores:
                total_score += scores[key] * weight
        
        return min(100, total_score)
    
    def _generate_gap_analysis(self, skill_analysis: Dict) -> Dict[str, Any]:
        """Generate detailed skill gap analysis"""
        missing_skills = skill_analysis.get('missing_skills', [])
        
        categorized_gaps = {
            'technical': [],
            'soft_skills': [],
            'programming': [],
            'other': []
        }
        
        for skill in missing_skills:
            categorized = False
            for category, skills_list in self.skill_keywords.items():
                if skill in skills_list:
                    if category == 'soft_skills':
                        categorized_gaps['soft_skills'].append(skill)
                    else:
                        categorized_gaps['technical'].append(skill)
                    categorized = True
                    break
            
            if not categorized:
                categorized_gaps['other'].append(skill)
        
        return {
            'categorized_gaps': categorized_gaps,
            'gap_severity': 'low' if len(missing_skills) <= 3 else 'medium' if len(missing_skills) <= 7 else 'high'
        }
    
    def _generate_recommendations(self, missing_skills: List[str], job_requirements: Dict) -> Dict[str, Any]:
        """Generate learning recommendations"""
        recommendations = {
            'courses': [],
            'projects': [],
            'certifications': [],
            'learning_path': []
        }
        
        for skill in missing_skills[:10]:
            recommendations['learning_path'].append({
                'skill': skill,
                'priority': 'high' if skill in ['python', 'java', 'sql', 'aws'] else 'medium',
                'estimated_time': '4-6 weeks',
                'difficulty': 'intermediate'
            })
            
            recommendations['courses'].append({
                'name': f'Complete {skill} Course',
                'platform': 'Online'
            })
            
            recommendations['projects'].append({
                'name': f'Build with {skill}',
                'description': f'Hands-on project using {skill}'
            })
            
            recommendations['certifications'].append({
                'name': f'{skill} Certification'
            })
        
        return recommendations