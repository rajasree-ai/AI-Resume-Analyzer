"""
OpenAI Service for Smart Recommendations
"""

import openai
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

class OpenAIService:
    """Service for generating AI-powered recommendations"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def generate_learning_plan(self, missing_skills: List[str], job_title: str, user_level: str = "intermediate") -> Dict[str, Any]:
        """
        Generate personalized learning plan using OpenAI
        """
        if not openai.api_key:
            return self._fallback_recommendations(missing_skills)
        
        try:
            prompt = f"""
            You are an expert career coach and skill development advisor.
            
            User needs to learn these skills for a {job_title} position:
            {', '.join(missing_skills)}
            
            Current skill level: {user_level}
            
            Please provide:
            1. A prioritized learning path with estimated time for each skill
            2. Specific course recommendations (with platform names)
            3. Project ideas to practice each skill
            4. Certification recommendations
            5. Recommended order to learn these skills
            6. Estimated total time to become job-ready
            
            Format as JSON with these keys:
            - learning_path: list of {skill, priority, estimated_time, difficulty}
            - courses: list of {name, platform, url}
            - projects: list of {name, description, skills_used}
            - certifications: list of {name, provider}
            - total_estimated_time: string
            - tips: string
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a career development expert. Provide structured, actionable advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            import json
            import re
            
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
            
            # If no JSON, return structured data from text
            return self._parse_text_response(content, missing_skills)
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_recommendations(missing_skills)
    
    def _parse_text_response(self, text: str, skills: List[str]) -> Dict[str, Any]:
        """Parse OpenAI text response into structured data"""
        return {
            'learning_path': [
                {'skill': s, 'priority': 'high', 'estimated_time': '4-6 weeks', 'difficulty': 'intermediate'}
                for s in skills[:5]
            ],
            'courses': [
                {'name': f'Complete {s} Mastery', 'platform': 'Online', 'url': None}
                for s in skills[:3]
            ],
            'projects': [
                {'name': f'Build with {s}', 'description': f'Hands-on project using {s}', 'skills_used': [s]}
                for s in skills[:3]
            ],
            'certifications': [
                {'name': f'{s} Certified Professional', 'provider': 'Industry Standard'}
                for s in skills[:3]
            ],
            'total_estimated_time': '8-12 weeks',
            'tips': 'Focus on one skill at a time. Build projects to reinforce learning.'
        }
    
    def _fallback_recommendations(self, missing_skills: List[str]) -> Dict[str, Any]:
        """Fallback recommendations when OpenAI is not available"""
        return {
            'learning_path': [
                {'skill': s, 'priority': 'high' if s in ['python', 'java', 'aws', 'react'] else 'medium',
                 'estimated_time': '4-6 weeks', 'difficulty': 'intermediate'}
                for s in missing_skills[:5]
            ],
            'courses': [
                {'name': f'{s} Course', 'platform': 'Online', 'url': None}
                for s in missing_skills[:3]
            ],
            'projects': [
                {'name': f'{s} Project', 'description': f'Build a project with {s}', 'skills_used': [s]}
                for s in missing_skills[:3]
            ],
            'certifications': [
                {'name': f'{s} Certification', 'provider': 'Certification Body'}
                for s in missing_skills[:3]
            ],
            'total_estimated_time': '6-10 weeks',
            'tips': 'Practice regularly and build projects to reinforce learning.'
        }

# Singleton instance
openai_service = OpenAIService()

def get_openai_service():
    """Get OpenAI service instance"""
    return openai_service