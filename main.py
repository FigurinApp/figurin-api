from flask import Flask
from flask_cors import CORS
from database.app import db, init_db
from routes.auth import auth_bp
from routes.test import test_bp  # rota de teste opcional

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua-chave-secreta'

# CORS para permitir o frontend acessar
CORS(app, origins=["http://localhost:5173", "https://figurin-app.onrender.com"], supports_credentials=True)

# Inicializa DB e Blueprint
db.init_app(app)
init_db(app)

# Registra rotas
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(test_bp, url_prefix='/api')  # opcional

# Executa localmente (Render ignora isso)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
