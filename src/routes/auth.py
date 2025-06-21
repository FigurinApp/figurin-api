from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models.user import User, db
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Email e senha obrigatórios"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"message": "Credenciais inválidas"}), 401

        payload = {
            "user_id": user.id,
            "email": user.email,
            "is_admin": user.is_admin,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }

        token = jwt.encode(payload, os.getenv("SECRET_KEY", "asdf#FGSgvasgf$5$WGT"), algorithm="HS256")

        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "is_admin": user.is_admin
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
