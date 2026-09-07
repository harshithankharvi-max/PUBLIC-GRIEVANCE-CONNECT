"""
Authorization Decorators for Role-Based Access Control
"""

from functools import wraps
from flask import session, redirect, url_for, jsonify, request

def admin_required(f):
    """Decorator to protect admin-only routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized', 'success': False}), 401
            return redirect(url_for('admin_login'))
        
        if session.get('role') != 'admin':
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Forbidden - Admin access required', 'success': False}), 403
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def citizen_required(f):
    """Decorator to protect citizen-only routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized', 'success': False}), 401
            return redirect(url_for('phone_login'))
        
        if session.get('role') != 'citizen':
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Forbidden - Citizen access required', 'success': False}), 403
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    
    return decorated_function


def login_required(f):
    """Generic login required decorator for both citizen and admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized', 'success': False}), 401
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    
    return decorated_function
