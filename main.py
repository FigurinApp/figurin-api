from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database.app import db
from routes.auth import auth_bp
from routes.user import user_bp
from routes.categories import categories_bp
from routes.stickers import stickers_bp
import os

app = Flask(__name__)
CORS(app, origins=["https://figurin-app.onrender.com", "http://localhost:5173"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret')

db.init_app(app)
jwt = JWTManager(app)

# Registra blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(categories_bp, url_prefix='/api')
app.register_blueprint(stickers_bp, url_prefix='/api')

# Cria o banco na primeira execução
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return 'API FigurinApp funcionando!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
