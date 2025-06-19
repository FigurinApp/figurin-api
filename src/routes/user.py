from flask import Blueprint, request, jsonify, session
from src.models.user import db, User

user_bp = Blueprint('user', __name__)

def require_admin():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    if not session.get('is_admin', False):
        return jsonify({'error': 'Admin access required'}), 403
    return None

@user_bp.route('/users', methods=['GET'])
def get_users():
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users', methods=['POST'])
def create_user():
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=username, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin')
    
    if username:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Username already exists'}), 400
        user.username = username
    
    if password:
        user.set_password(password)
    
    if is_admin is not None:
        user.is_admin = is_admin
    
    db.session.commit()
    
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200

