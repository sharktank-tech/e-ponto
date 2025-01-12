from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db)
login_manager = LoginManager()

def create_app():
    # Criação da instancia do Flask
    app = Flask(__name__)

    # Configuração da aplicação
    app.config.from_object('config.Config')

    # Inicizalizar as extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Define a rota padrão de login
    login_manager.login_view = 'main.login'  # Atualize 'auth.login' com sua rota real de login
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'

    # Registrar blueprints
    from web.views.routes import main_blueprint
    from web.views.admin_routes import admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)

    # Define o carregador de usuário para o LoginManager
    from web.modules.models import Users  # Certifique-se de que o modelo User está no módulo correto

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app