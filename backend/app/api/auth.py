"""
Authentication API Routes
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import re
import jwt
import os
import hashlib

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# =============================================
# HELPER FUNCTIONS
# =============================================

def generate_auth_token(user_id, expires_in=7):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=expires_in)
    }
    return jwt.encode(payload, os.environ.get('SECRET_KEY', 'dev-key'), algorithm='HS256')

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password"""
    return hash_password(password) == password_hash

# =============================================
# REGISTER ENDPOINT
# =============================================

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        required = ['username', 'email', 'password']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({'error': f'Missing: {", ".join(missing)}'}), 400
        
        username = data.get('username').strip()
        email = data.get('email').strip().lower()
        password = data.get('password')
        full_name = data.get('full_name', '').strip()
        
        # Validate
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return jsonify({'error': 'Invalid username format'}), 400
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'error': 'Invalid email format'}), 400
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check existing users (in-memory for demo)
        app = current_app
        for user in app.users.values():
            if user['username'] == username:
                return jsonify({'error': 'Username already taken'}), 400
            if user['email'] == email:
                return jsonify({'error': 'Email already registered'}), 400
        
        # Create user
        user_id = app.user_id_counter
        app.user_id_counter += 1
        
        user = {
            'id': user_id,
            'username': username,
            'email': email,
            'password_hash': hash_password(password),
            'full_name': full_name,
            'bio': None,
            'is_active': True,
            'is_admin': False,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'last_login': None
        }
        
        app.users[user_id] = user
        
        token = generate_auth_token(user_id)
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'id': user_id,
                'username': username,
                'email': email,
                'full_name': full_name
            },
            'token': token
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

# =============================================
# LOGIN ENDPOINT
# =============================================

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        app = current_app
        user = None
        for u in app.users.values():
            if u['email'] == email:
                user = u
                break
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not verify_password(password, user['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user['is_active']:
            return jsonify({'error': 'Account deactivated'}), 401
        
        user['last_login'] = datetime.utcnow().isoformat()
        
        token = generate_auth_token(user['id'])
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name']
            },
            'token': token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

# =============================================
# GET CURRENT USER
# =============================================

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        app = current_app
        user = app.users.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'bio': user.get('bio'),
                'is_active': user['is_active'],
                'created_at': user['created_at']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================
# LOGOUT
# =============================================

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    }), 200