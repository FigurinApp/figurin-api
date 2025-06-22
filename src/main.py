from flask import Flask
from flask_cors import CORS
from models.user import db
from routes.auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

CORS(app, supports_credentials=True)
db.init_app(app)

# Registra as rotas de autenticação
app.register_blueprint(auth_bp, url_prefix='/api')

@app.route('/')
def home():
    return 'API do FigurinApp está rodando.'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
