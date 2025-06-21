from flask import Blueprint, jsonify

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(["Esportes", "Filmes", "Séries"])


