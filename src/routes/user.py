from flask import Blueprint, jsonify
from models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([
        {"id": user.id, "email": user.email, "is_admin": user.is_admin}
        for user in users
    ])

