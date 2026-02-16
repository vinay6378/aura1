# deploy_admin_setup.py
# One-time script to set up admin account on Render
import requests
import json

def setup_admin_on_render():
    """Set up admin account on your Render deployment"""
    
    # Your Render app URL (replace with actual URL)
    render_url = "https://your-app-name.onrender.com"
    
    # Admin credentials
    admin_data = {
        "username": "vinay",
        "email": "vs8890864@gmail.com", 
        "password": "admin123",  # Change this to a secure password
        "confirm_password": "admin123"
    }
    
    try:
        # Create admin account
        response = requests.post(f"{render_url}/setup-admin", data=admin_data)
        
        if response.status_code == 200:
            print("✅ Admin account created successfully!")
            print(f"🌐 Admin Dashboard: {render_url}/admin/dashboard")
            print(f"📧 Email: {admin_data['email']}")
            print(f"👤 Username: {admin_data['username']}")
            print("🔐 Password: admin123 (change this immediately!)")
        else:
            print(f"❌ Failed to create admin: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n📝 Manual Setup Instructions:")
        print(f"1. Visit: {render_url}/setup-admin")
        print(f"2. Use these credentials:")
        print(f"   - Email: {admin_data['email']}")
        print(f"   - Username: {admin_data['username']}")
        print(f"   - Password: admin123")
        print("3. Change your password immediately after login")

if __name__ == "__main__":
    setup_admin_on_render()
