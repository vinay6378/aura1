# app.py
from flask import Flask, redirect
from extensions import db, login_manager, mail
from flask_migrate import Migrate
from models import User, Event   # Import User and Event models
import os

def create_app():
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
    
    # Production/Development configuration
    if os.getenv('FLASK_ENV') == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
    else:
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
    
    #  CONFIGURE DATABASE
    if os.getenv("DATABASE_URL"):
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aura.db"
    
    # Production settings
    if os.getenv("RENDER"):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Email Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'gautamvinay939@gmail.com')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')  # Set this in environment
    app.config['MAIL_DEFAULT_SENDER'] = ('Aura', 'gautamvinay939@gmail.com')
    
    # Initialize extensions
    from extensions import init_extensions
    init_extensions(app)
    
    # Flask-Migrate initialization
    migrate = Migrate(app, db)

     #  IMPORT MODELS (CRITICAL)
    import models

    #  CREATE TABLES
    with app.app_context():
        db.create_all()

    # Register blueprints
    from main.routes import bp as main_bp
    from auth.routes import auth_bp
    from admin.routes import admin_bp
    from api.routes import api_bp
    
    app.register_blueprint(main_bp)
    
    @app.route('/login')
    def login_redirect():
        return redirect('/auth/login')
    
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")
    
    # Global context processor to make admin_exists available in all templates
    @app.context_processor
    def inject_admin_exists():
        with app.app_context():
            from models import User
            admin_exists = User.query.filter_by(is_admin=True).first() is not None
            return dict(admin_exists=admin_exists)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
