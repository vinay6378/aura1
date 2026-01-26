from app import create_app
from models import User, db

app = create_app()

with app.app_context():
    # Check all users in database
    all_users = User.query.all()
    
    print("🔍 Debugging User Accounts:")
    print(f"Total users found: {len(all_users)}")
    
    for user in all_users:
        print(f"\n👤 User ID: {user.id}")
        print(f"📧 Email: {user.email}")
        print(f"👤 Username: {user.username}")
        print(f"👑 Is Admin: {user.is_admin}")
        print(f"✅ Is Active: {user.is_active}")
        print(f"🔐 Has Password Hash: {'Yes' if user.password_hash else 'No'}")
        
        if user.password_hash:
            print(f"🔐 Password Hash Length: {len(user.password_hash)}")
            print(f"🔐 Password Hash: {user.password_hash[:20]}...")
        else:
            print("❌ No password hash found!")
    
    print("\n🌐 To test login:")
    print("1. Run: python app.py")
    print("2. Go to: http://127.0.0.1:5000/auth/login")
    print("3. Use any existing user credentials")
    
    print("\n🔧 To manage admin account:")
    print("1. Run: python manage_admin.py")
    print("2. Choose option to view or update admin details")
