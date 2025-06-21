from flask import Blueprint, jsonify

stickers_bp = Blueprint('stickers', __name__)

# Rota de exemplo para listar figurinhas
@stickers_bp.route('/stickers', methods=['GET'])
def get_stickers():
    mock_stickers = [
        {"id": 1, "name": "Sticker A"},
        {"id": 2, "name": "Sticker B"},
        {"id": 3, "name": "Sticker C"},
    ]
    return jsonify(mock_stickers)
