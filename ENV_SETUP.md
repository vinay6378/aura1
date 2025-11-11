# Environment Setup Guide

## Email Configuration

To enable email notifications when contact forms are submitted, you need to set up Gmail App Password.

### Steps:

1. **Generate Gmail App Password:**
   - Go to your Google Account settings
   - Navigate to Security > 2-Step Verification > App Passwords
   - Generate a new app password for "Mail"
   - Copy the 16-character password

2. **Set Environment Variables:**

   **For local development (Windows):**
   ```cmd
   set MAIL_PASSWORD=your_app_password_here
   set MAIL_USERNAME=gautamvinay939@gmail.com
   set SECRET_KEY=your_secret_key_here
   ```

   **For production (Linux/Mac):**
   ```bash
   export MAIL_PASSWORD=your_app_password_here
   export MAIL_USERNAME=gautamvinay939@gmail.com
   export SECRET_KEY=your_secret_key_here
   ```

   **Or create a `.env` file in the project root:**
   ```
   MAIL_PASSWORD=your_app_password_here
   MAIL_USERNAME=gautamvinay939@gmail.com
   SECRET_KEY=your_secret_key_here
   ```

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Access the website:
   - Open http://localhost:5000 in your browser

## Features Implemented

✅ **Email Integration** - Contact form submissions sent to gautamvinay939@gmail.com
✅ **AI Chatbot** - Floating AI assistant widget on every page
✅ **3D Models** - Spline 3D models integrated with Lenis smooth scrolling
✅ **Modern Theme** - Purple/Pink gradient theme with advanced animations
✅ **GSAP Animations** - Smooth scroll triggers and hover effects
✅ **Custom Cursor** - Interactive cursor effects
✅ **Responsive Design** - Mobile-friendly across all devices

## Contact Form

When someone fills out the contact form:
1. All details are saved to the database
2. An email is automatically sent to gautamvinay939@gmail.com with all details
3. A success message is shown to the user

## AI Chatbot

- Click the robot icon in the bottom-right corner
- Ask questions about services, pricing, etc.
- Powered by intelligent responses

