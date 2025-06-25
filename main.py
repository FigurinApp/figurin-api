from flask import Flask
from flask_cors import CORS
from database.app import db
from routes.auth import auth_bp
from routes.categories import categories_bp
from routes.user import user_bp
from routes.stickers import stickers_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secreta'

db.init_app(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Libera CORS

# Registro das rotas
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(categories_bp, url_prefix='/api')
app.register_blueprint(stickers_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
