"""
Flask Application Factory
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """Create and configure the Flask application"""
    
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    frontend_folder = os.path.join(project_root, 'frontend')
    
    app = Flask(__name__, 
                static_folder=frontend_folder,
                static_url_path='/static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}
    app.config['FRONTEND_FOLDER'] = frontend_folder
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', app.config['SECRET_KEY'])
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'json']
    
    # Initialize extensions
    jwt = JWTManager(app)
    CORS(app, origins='*', supports_credentials=True)
    
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('backend/data', exist_ok=True)
    
    # =============================================
    # IN-MEMORY STORAGE (for demo purposes)
    # =============================================
    app.users = {}
    app.resumes = {}
    app.analyses = {}
    app.jobs = {}
    app.user_id_counter = 1
    app.resume_id_counter = 1
    app.analysis_id_counter = 1
    app.job_id_counter = 1
    
    # =============================================
    # Register blueprints - SIMPLE IMPORT
    # =============================================
    try:
        from app.api.auth import auth_bp
        app.register_blueprint(auth_bp)
        print("✅ Auth blueprint loaded")
    except ImportError:
        try:
            from api.auth import auth_bp
            app.register_blueprint(auth_bp)
            print("✅ Auth blueprint loaded (alt)")
        except ImportError as e:
            print(f"⚠️  Could not load auth blueprint: {e}")
    
    try:
        from app.api.resume import resume_bp
        app.register_blueprint(resume_bp)
        print("✅ Resume blueprint loaded")
    except ImportError:
        try:
            from api.resume import resume_bp
            app.register_blueprint(resume_bp)
            print("✅ Resume blueprint loaded (alt)")
        except ImportError as e:
            print(f"⚠️  Could not load resume blueprint: {e}")
    
    try:
        from app.api.analysis import analysis_bp
        app.register_blueprint(analysis_bp)
        print("✅ Analysis blueprint loaded")
    except ImportError:
        try:
            from api.analysis import analysis_bp
            app.register_blueprint(analysis_bp)
            print("✅ Analysis blueprint loaded (alt)")
        except ImportError as e:
            print(f"⚠️  Could not load analysis blueprint: {e}")
    
    # =============================================
    # SERVE FRONTEND
    # =============================================
    
    @app.route('/')
    def serve_index():
        frontend_path = app.config.get('FRONTEND_FOLDER', '')
        index_path = os.path.join(frontend_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(frontend_path, 'index.html')
        return jsonify({'error': 'index.html not found'}), 404
    
    @app.route('/<path:path>')
    def serve_static(path):
        frontend_path = app.config.get('FRONTEND_FOLDER', '')
        file_path = os.path.join(frontend_path, path)
        if os.path.exists(file_path):
            return send_from_directory(frontend_path, path)
        return jsonify({'error': f'File not found: {path}'}), 404
    
    @app.route('/api', methods=['GET'])
    def api_info():
        return jsonify({
            'name': 'AI Resume Skill Gap Analyzer',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'register': '/api/auth/register',
                'login': '/api/auth/login',
                'profile': '/api/auth/me',
                'upload': '/api/resume/upload',
                'analyze': '/api/analysis/analyze/<resume_id>'
            }
        }), 200
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'AI Resume Skill Gap Analyzer is running'
        }), 200
    
    return app