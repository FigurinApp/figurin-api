from flask import Flask
from flask_cors import CORS

# Blueprints das rotas
from routes.auth       import auth_bp
from routes.user       import user_bp
from routes.categories import categories_bp
from routes.stickers   import stickers_bp
from routes.test       import test_bp

def create_app():
    app = Flask(__name__)

    # Permite chamadas do frontend a qualquer rota /api/*
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registro de blueprints com prefixo /api
    app.register_blueprint(auth_bp,       url_prefix='/api')
    app.register_blueprint(user_bp,       url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')
    app.register_blueprint(stickers_bp,   url_prefix='/api')
    app.register_blueprint(test_bp,       url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    # roda em 0.0.0.0 para aceitar conexões externas (p.ex. no Render)
    app.run(host='0.0.0.0', port=5000)
