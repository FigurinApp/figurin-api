from flask import Blueprint, jsonify

stickers_bp = Blueprint('stickers', __name__)

@stickers_bp.route('/stickers', methods=['GET'])
def get_stickers():
    return jsonify([
        {"id": 1, "name": "Sticker 1"},
        {"id": 2, "name": "
