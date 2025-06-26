from flask import Flask
from flask_cors import CORS
from database.app import db, Base, engine
from routes.auth import auth_bp
from routes.test import test_bp  # Rota de teste opcional

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db.init_app(app)

# Garante que as tabelas estão criadas
with app.app_context():
    Base.metadata.create_all(bind=engine)

# Libera CORS apenas para o frontend hospedado
CORS(app, origins=["https://figurin-app.onrender.com"], supports_credentials=True)

# Registra as rotas (blueprints)
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(test_bp, url_prefix='/api')  # rota /api/test

# Inicia o app
if __name__ == '__main__':
    app.run(debug=True)
