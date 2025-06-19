from flask import Blueprint, request, jsonify, session
from src.models.user import db, Category

categories_bp = Blueprint('categories', __name__)

def require_auth():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    return None

def require_admin():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    if not session.get('is_admin', False):
        return jsonify({'error': 'Admin access required'}), 403
    return None

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories]), 200

@categories_bp.route('/categories', methods=['POST'])
def create_category():
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Category name is required'}), 400
    
    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'Category already exists'}), 400
    
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    
    return jsonify(category.to_dict()), 201

@categories_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Category name is required'}), 400
    
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category and existing_category.id != category_id:
        return jsonify({'error': 'Category name already exists'}), 400
    
    category.name = name
    db.session.commit()
    
    return jsonify(category.to_dict()), 200

@categories_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Category deleted successfully'}), 200

