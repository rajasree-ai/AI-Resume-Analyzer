import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///resume_analyzer.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # OpenAI API (optional)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Model paths
    MODEL_PATH = 'models/'
    SKILL_MODEL_PATH = os.path.join(MODEL_PATH, 'skill_model.pkl')
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # Skill categories
    SKILL_CATEGORIES = {
        'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift'],
        'web_development': ['react', 'angular', 'vue', 'node.js', 'html', 'css', 'javascript'],
        'data_science': ['python', 'r', 'sql', 'pandas', 'numpy', 'scikit-learn', 'tensorflow'],
        'soft_skills': ['communication', 'leadership', 'teamwork', 'problem-solving', 'adaptability']
    }
    
    # ATS keywords for optimization
    ATS_KEYWORDS = ['experienced', 'proficient', 'skilled', 'expert', 'professional', 
                    'certified', 'bachelor', 'master', 'degree']