import re
from typing import List, Dict, Set, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

class SkillAnalyzer:
    def __init__(self):
        # Load pre-trained model for skill embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Predefined skill categories
        self.skill_categories = {
            'programming': ['python', 'java', 'c++', 'javascript', 'ruby', 'go', 'rust', 
                          'swift', 'kotlin', 'typescript', 'php', 'perl', 'scala'],
            'web_development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 
                              'express', 'django', 'flask', 'spring', 'asp.net'],
            'data_science': ['python', 'r', 'sql', 'pandas', 'numpy', 'scikit-learn',
                           'tensorflow', 'pytorch', 'keras', 'matplotlib', 'seaborn',
                           'power bi', 'tableau'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
                     'jenkins', 'gitlab', 'github actions'],
            'soft_skills': ['communication', 'leadership', 'teamwork', 'problem-solving',
                          'critical thinking', 'adaptability', 'time management',
                          'project management', 'presentation', 'negotiation']
        }
        
        # Load common industry skills
        with open('data/skills_database.json', 'r') as f:
            self.industry_skills = json.load(f)
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Remove common stopwords and punctuation
        text = re.sub(r'[^\w\s]', '', text.lower())
        words = text.split()
        
        # Technical keywords patterns
        tech_patterns = [
            r'\b\w+\.?\w*[^\s]*\b',  # Words with dots (like .NET, node.js)
            r'\b[A-Z]+[A-Z0-9_-]*\b'  # Acronyms
        ]
        
        keywords = []
        for pattern in tech_patterns:
            keywords.extend(re.findall(pattern, text))
        
        return list(set([w for w in keywords if len(w) > 2]))
    
    def match_skills(self, resume_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
        """Match resume skills against job requirements"""
        resume_skills = [s.lower().strip() for s in resume_skills]
        job_skills = [s.lower().strip() for s in job_skills]
        
        # Find exact matches
        exact_matches = set(resume_skills) & set(job_skills)
        
        # Find semantic matches using embeddings
        semantic_matches = []
        if resume_skills and job_skills:
            resume_embeddings = self.model.encode(resume_skills)
            job_embeddings = self.model.encode(job_skills)
            
            similarity_matrix = cosine_similarity(resume_embeddings, job_embeddings)
            
            for i, resume_skill in enumerate(resume_skills):
                for j, job_skill in enumerate(job_skills):
                    if similarity_matrix[i][j] > 0.7 and resume_skill not in exact_matches:
                        semantic_matches.append({
                            'resume_skill': resume_skill,
                            'job_skill': job_skill,
                            'similarity': float(similarity_matrix[i][j])
                        })
        
        # Find missing skills
        all_job_skills = set(job_skills)
        matching_skills = set(exact_matches) | set([m['job_skill'] for m in semantic_matches])
        missing_skills = all_job_skills - matching_skills
        
        return {
            'exact_matches': list(exact_matches),
            'semantic_matches': semantic_matches,
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'match_rate': len(matching_skills) / len(all_job_skills) if all_job_skills else 0
        }
    
    def categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into different domains"""
        categorized = {category: [] for category in self.skill_categories.keys()}
        categorized['other'] = []
        
        for skill in skills:
            skill_lower = skill.lower()
            found = False
            
            for category, category_skills in self.skill_categories.items():
                if skill_lower in category_skills:
                    categorized[category].append(skill)
                    found = True
                    break
            
            if not found:
                categorized['other'].append(skill)
        
        return categorized
    
    def calculate_skill_score(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Calculate skill score based on relevance"""
        if not job_skills:
            return 0.0
        
        match_result = self.match_skills(resume_skills, job_skills)
        return match_result['match_rate'] * 100
    
    def get_skill_recommendations(self, missing_skills: List[str], user_level: str = 'intermediate') -> List[Dict[str, Any]]:
        """Get recommendations for missing skills"""
        recommendations = []
        
        for skill in missing_skills:
            # Find related resources
            resources = self._find_skill_resources(skill, user_level)
            
            recommendations.append({
                'skill': skill,
                'importance': 'high' if skill in self.skill_categories.get('programming', []) else 'medium',
                'learning_resources': resources,
                'estimated_time': self._estimate_learning_time(skill),
                'difficulty': self._assess_difficulty(skill)
            })
        
        return recommendations
    
    def _find_skill_resources(self, skill: str, level: str) -> List[Dict[str, str]]:
        """Find learning resources for a skill"""
        resources = []
        
        # This would typically query a database or API for courses
        # For now, return simulated resources
        resources = [
            {
                'type': 'course',
                'name': f'Mastering {skill}',
                'platform': 'Coursera',
                'url': f'https://coursera.org/courses/{skill.lower().replace(" ", "-")}'
            },
            {
                'type': 'course',
                'name': f'{skill} for {level}',
                'platform': 'Udemy',
                'url': f'https://udemy.com/courses/{skill.lower().replace(" ", "-")}'
            }
        ]
        
        return resources
    
    def _estimate_learning_time(self, skill: str) -> str:
        """Estimate learning time for a skill"""
        if skill in self.skill_categories.get('programming', []):
            return '4-8 weeks'
        elif skill in self.skill_categories.get('soft_skills', []):
            return '2-4 weeks'
        else:
            return '3-6 weeks'
    
    def _assess_difficulty(self, skill: str) -> str:
        """Assess difficulty level of learning a skill"""
        if skill in ['python', 'javascript', 'html', 'css']:
            return 'beginner'
        elif skill in ['react', 'node.js', 'sql', 'java']:
            return 'intermediate'
        elif skill in ['tensorflow', 'kubernetes', 'aws']:
            return 'advanced'
        else:
            return 'intermediate'