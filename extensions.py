# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os

db = SQLAlchemy()
mail = Mail()

def init_extensions(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail settings (we’ll configure next)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'vs8890864@gmail.com'
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # from Render env vars
    app.config['MAIL_DEFAULT_SENDER'] = 'vs8890864@gmail.com'

    db.init_app(app)
    mail.init_app(app)

