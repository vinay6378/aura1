# seed_admin.py
# Script to create admin account automatically on deployment
from app import create_app
from models import User, db
import os

def create_admin_account():
    """Create admin account if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(is_admin=True).first()
        
        if existing_admin:
            print(f"✅ Admin account already exists: {existing_admin.email}")
            return existing_admin
        
        # Get admin credentials from environment variables
        admin_email = os.getenv('ADMIN_EMAIL', 'vs8890864@gmail.com')
        admin_username = os.getenv('ADMIN_USERNAME', 'vinay')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        # Create admin user
        admin_user = User(
            username=admin_username,
            email=admin_email,
            is_admin=True,
            is_active=True
        )
        admin_user.set_password(admin_password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"👑 Admin account created successfully!")
        print(f"📧 Email: {admin_email}")
        print(f"👤 Username: {admin_username}")
        print(f"🔐 Password: {admin_password}")
        print(f"🌐 Admin URL: https://your-app.onrender.com/admin/dashboard")
        
        return admin_user

if __name__ == '__main__':
    create_admin_account()
