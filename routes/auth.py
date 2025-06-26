from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from database.app import SessionLocal
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)
db = SessionLocal()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Dados ausentes"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email e senha são obrigatórios"}), 400

    user = db.query(User).filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(token=access_token), 200  # <-- frontend espera isso
    return jsonify({"msg": "Credenciais inválidas"}), 401
