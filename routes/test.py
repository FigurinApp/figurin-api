from flask import Blueprint, jsonify
from database.app import SessionLocal
from models.user import User

test_bp = Blueprint('test', __name__)

@test_bp.route('/api/create-admin', methods=['GET'])
def create_admin():
    db = SessionLocal()
    if db.query(User).filter_by(email="admin@figurinapp.com").first():
        return jsonify({"msg": "Admin já existe"}), 400

    admin = User(email="admin@figurinapp.com", is_admin=True)
    admin.set_password("SenhaForte123")
    db.add(admin)
    db.commit()
    db.close()
    return jsonify({"msg": "Admin criado com sucesso"}), 201
