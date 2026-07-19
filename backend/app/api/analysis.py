"""
Analysis API
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

def extract_skills_from_text(text):
    """Extract skills from text"""
    skills = []
    common_skills = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
        'html', 'css', 'sql', 'mongodb', 'postgresql', 'mysql', 'docker',
        'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'tensorflow',
        'pytorch', 'scikit-learn', 'pandas', 'numpy', 'django', 'flask',
        'spring', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin'
    ]
    
    text_lower = text.lower()
    for skill in common_skills:
        if skill in text_lower:
            skills.append(skill)
    
    return skills

@analysis_bp.route('/analyze/<int:resume_id>', methods=['POST'])
def analyze_resume(resume_id):
    try:
        app = current_app
        resume = app.resumes.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        job_description = data.get('job_description', '')
        if not job_description:
            return jsonify({'error': 'Job description required'}), 400
        
        # Extract skills from job description
        job_skills = extract_skills_from_text(job_description)
        resume_skills = resume.get('skills', [])
        
        # Find matching skills
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        matching = [s for s in resume_skills if s.lower() in job_skills_lower]
        missing = [s for s in job_skills if s.lower() not in resume_skills_lower]
        
        # Calculate score
        total = len(job_skills_lower) or 1
        overall_score = round((len(matching) / total) * 100)
        
        # Create analysis record
        analysis_id = app.analysis_id_counter
        app.analysis_id_counter += 1
        
        # Create job record
        job_id = app.job_id_counter
        app.job_id_counter += 1
        
        job = {
            'id': job_id,
            'title': data.get('job_title', 'Unknown'),
            'company': data.get('company', 'Unknown'),
            'description': job_description,
            'skills': job_skills,
            'created_at': datetime.utcnow().isoformat()
        }
        app.jobs[job_id] = job
        
        analysis = {
            'id': analysis_id,
            'resume_id': resume_id,
            'job_id': job_id,
            'overall_score': overall_score,
            'matching_skills': matching,
            'missing_skills': missing,
            'resume_skills': resume_skills,
            'job_skills': job_skills,
            'created_at': datetime.utcnow().isoformat()
        }
        app.analyses[analysis_id] = analysis
        
        return jsonify({
            'analysis_id': analysis_id,
            'overall_score': overall_score,
            'keyword_match': round(overall_score * 0.85),
            'experience_match': 70,
            'education_match': 75,
            'matching_skills': matching,
            'missing_skills': missing,
            'skill_analysis': {
                'match_score': overall_score,
                'total_job_skills': len(job_skills),
                'total_resume_skills': len(resume_skills)
            },
            'recommendations': {
                'courses': [{'name': f'Learn {s}', 'platform': 'Online'} for s in missing[:5]],
                'projects': [{'name': f'Build with {s}', 'description': 'Hands-on project'} for s in missing[:3]],
                'certifications': [{'name': f'{s} Certification'} for s in missing[:3]]
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500