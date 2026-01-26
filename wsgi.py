# wsgi.py - Production WSGI entry point
import os
from app import create_app

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Create the Flask application
app = create_app()

# Production WSGI application
application = app

if __name__ == "__main__":
    # For local development only
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
