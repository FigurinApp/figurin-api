import os
import sys
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from models.user import db
from routes.auth import auth_bp
from routes.user import user_bp
from routes.categories import categories_bp
from routes.stickers import stickers_bp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "asdf#FGSgvasgf$5$WGT")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS habilitado para aceitar cookies/credenciais
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})

# Blueprints
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(categories_bp, url_prefix="/api")
app.register_blueprint(stickers_bp, url_prefix="/api")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        return send_from_directory(static_folder_path, 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
