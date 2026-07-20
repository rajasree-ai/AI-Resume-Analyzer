"""
Resume Upload API
"""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import re
from datetime import datetime

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

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

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'docx', 'txt'})
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed:
            return jsonify({'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Extract skills from filename (simple demo)
        skills = extract_skills_from_text(filename)
        if not skills:
            skills = ['Python', 'JavaScript', 'SQL', 'Git', 'React', 'Node.js']
        
        # Get app instance
        app = current_app
        
        # Ensure resumes dict exists
        if not hasattr(app, 'resumes'):
            app.resumes = {}
        if not hasattr(app, 'resume_id_counter'):
            app.resume_id_counter = 1
        
        # Create resume record
        resume_id = app.resume_id_counter
        app.resume_id_counter += 1
        
        resume = {
            'id': resume_id,
            'filename': filename,
            'file_path': file_path,
            'file_size': os.path.getsize(file_path),
            'file_type': filename.rsplit('.', 1)[1].lower(),
            'skills': skills,
            'is_processed': True,
            'upload_date': datetime.utcnow().isoformat()
        }
        
        app.resumes[resume_id] = resume
        print(f"✅ Resume uploaded: {filename} (ID: {resume_id})")
        
        return jsonify({
            'success': True,
            'message': 'Resume uploaded successfully',
            'resume_id': resume_id,
            'parsed_data': {
                'skills': skills,
                'skill_count': len(skills)
            }
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@resume_bp.route('/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    try:
        app = current_app
        
        if not hasattr(app, 'resumes'):
            app.resumes = {}
        
        resume = app.resumes.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        return jsonify({
            'id': resume['id'],
            'filename': resume['filename'],
            'upload_date': resume['upload_date'],
            'skills': resume.get('skills', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resume_bp.route('/list', methods=['GET'])
def list_resumes():
    try:
        app = current_app
        
        if not hasattr(app, 'resumes'):
            app.resumes = {}
        
        resumes = list(app.resumes.values())
        
        return jsonify({
            'resumes': [{
                'id': r['id'],
                'filename': r['filename'],
                'upload_date': r['upload_date'],
                'skill_count': len(r.get('skills', [])),
                'is_processed': r.get('is_processed', False)
            } for r in resumes]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500