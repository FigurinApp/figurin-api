from flask import Blueprint, request, jsonify, session
from src.models.user import db, Sticker, Category

stickers_bp = Blueprint('stickers', __name__)

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

@stickers_bp.route('/stickers', methods=['GET'])
def get_stickers():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    category_id = request.args.get('category_id')
    
    if category_id:
        stickers = Sticker.query.filter_by(category_id=category_id).all()
    else:
        stickers = Sticker.query.all()
    
    return jsonify([sticker.to_dict() for sticker in stickers]), 200

@stickers_bp.route('/stickers', methods=['POST'])
def create_sticker():
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    data = request.get_json()
    name = data.get('name')
    image_url = data.get('image_url')
    category_id = data.get('category_id')
    
    if not all([name, image_url, category_id]):
        return jsonify({'error': 'Name, image_url, and category_id are required'}), 400
    
    # Verify category exists
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    sticker = Sticker(name=name, image_url=image_url, category_id=category_id)
    db.session.add(sticker)
    db.session.commit()
    
    return jsonify(sticker.to_dict()), 201

@stickers_bp.route('/stickers/<int:sticker_id>', methods=['PUT'])
def update_sticker(sticker_id):
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    sticker = Sticker.query.get_or_404(sticker_id)
    data = request.get_json()
    
    name = data.get('name')
    image_url = data.get('image_url')
    category_id = data.get('category_id')
    
    if name:
        sticker.name = name
    if image_url:
        sticker.image_url = image_url
    if category_id:
        # Verify category exists
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        sticker.category_id = category_id
    
    db.session.commit()
    
    return jsonify(sticker.to_dict()), 200

@stickers_bp.route('/stickers/<int:sticker_id>', methods=['DELETE'])
def delete_sticker(sticker_id):
    admin_error = require_admin()
    if admin_error:
        return admin_error
    
    sticker = Sticker.query.get_or_404(sticker_id)
    db.session.delete(sticker)
    db.session.commit()
    
    return jsonify({'message': 'Sticker deleted successfully'}), 200

