from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models.database import Database
import os

load_dotenv()


def create_app():
    app = Flask(__name__)

    with app.app_context():
        Database.create_tables()
    
    app.secret_key = os.getenv('SECRET_KEY')
    if not app.secret_key:
        raise ValueError("SECRET_KEY not found in .env file!")

    # Security Settings
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Auto logout after 30 min inactivity

    # Extensions
    CSRFProtect(app)

    # Rate Limiter
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day"],
        storage_uri="memory://"
    )

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # User Loader
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # Blueprints
    from app.routes.auth import auth_bp
    from app.routes.productrout import product_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp)

    print("Secure Flask App Started Successfully!")
    return app