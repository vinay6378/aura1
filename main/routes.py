# main/routes.py
from flask import Blueprint, render_template,request, redirect, url_for, flash
from models import ContactMessage, Event, User
from extensions import db
from flask_login import login_user
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bp = Blueprint('main', __name__, template_folder='../templates')

def send_email_notification(name, email, subject, message):
    """Send email notification to owner when contact form is submitted"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = 'vs8890864@gmail.com'
        msg['To'] = 'vs8890864@gmail.com'
        msg['Subject'] = f'New Contact Form Submission: {subject}'
        
        # Create email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h2 style="color: white; margin: 0;">New Contact Form Submission</h2>
                </div>
                <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px;">
                    <h3 style="color: #667eea; margin-top: 0;">Contact Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Name:</strong></td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">{name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Email:</strong></td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">{email}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Subject:</strong></td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">{subject}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;"><strong>Message:</strong></td>
                            <td style="padding: 10px;">{message}</td>
                        </tr>
                    </table>
                    
                    <div style="margin-top: 30px; padding: 15px; background: #f0f4f8; border-left: 4px solid #667eea; border-radius: 5px;">
                        <p style="margin: 0; color: #666;">
                            <strong>Next Steps:</strong><br>
                            Please respond to this inquiry as soon as possible via: <a href="mailto:{email}" style="color: #667eea;">{email}</a>
                        </p>
                    </div>
                </div>
                <div style="text-align: center; padding: 20px; color: #999; font-size: 12px;">
                    <p>This is an automated message from Aura Contact System</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        if os.environ.get('MAIL_PASSWORD'):
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login('vs8890864@gmail.com', os.environ.get('MAIL_PASSWORD'))
            smtp_server.send_message(msg)
            smtp_server.quit()
        else:
            print("MAIL_PASSWORD not set - email not sent")
        
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

@bp.route('/')
def index():
    return render_template("index.html", title="Aura — One Company. Three Superpowers.")

@bp.route('/about')
def about():
    return render_template("about.html", title="About Us")

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', '')  # Optional field
        inquiry_type = request.form.get('inquiry_type', 'general')  # Get inquiry type
        message = request.form['message']
        
        # Create subject from inquiry type
        subject_map = {
            'general': 'General Inquiry',
            'web': 'Web Development Inquiry',
            'software': 'Software Development Inquiry',
            'marketing': 'Digital Marketing Inquiry',
            'support': 'Technical Support',
            'partnership': 'Partnership Opportunity'
        }
        subject = subject_map.get(inquiry_type, 'General Inquiry')
        
        # Save to database
        new_msg = ContactMessage(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        db.session.add(new_msg)
        db.session.commit()
        
        # Send email notification
        send_email_notification(name, email, subject, message)

        flash('Your message has been sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))

    return render_template('contact.html')

@bp.route('/ai-chat', methods=['POST'])
def ai_chat():
    """AI Chat endpoint for chatbot"""
    try:
        user_message = request.json.get('message', '')
        # Simple AI response logic - can be enhanced with OpenAI API
        responses = {
            'hi': 'Hello! How can I help you today?',
            'hello': 'Hi there! Welcome to Aura. How can we assist you?',
            'services': 'We offer web development, software development, and digital marketing services. Which interests you?',
            'price': 'Please contact us for customized pricing based on your requirements.',
            'default': 'Thank you for your message! Our team will get back to you shortly. For urgent inquiries, please email ''vs8890864@gmail.com'
        }
        
        user_lower = user_message.lower()
        for key in responses:
            if key in user_lower:
                return jsonify({'response': responses[key]})
        
        return jsonify({'response': responses['default']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/events')
def events():
    events = Event.query.all()
    return render_template("events.html", events=events)

@bp.route('/webdev')
def webdev():
    return render_template("webdev.html", title="Web Development")

@bp.route('/software')
def software():
    return render_template("software.html", title="Software Development")

@bp.route('/marketing')
def marketing():
    return render_template("marketing.html", title="Marketing Services")

# Digital Marketing Specific Routes
@bp.route('/seo')
def seo():
    return render_template("seo.html", title="SEO Services")

@bp.route('/social-media')
def social_media():
    return render_template("social_media.html", title="Social Media Marketing")

@bp.route('/ppc')
def ppc():
    return render_template("ppc.html", title="PPC & Google Ads")

@bp.route('/content-marketing')
def content_marketing():
    return render_template("content_marketing.html", title="Content Marketing")

@bp.route('/marketing-analytics')
def marketing_analytics():
    return render_template("marketing_analytics.html", title="Marketing Analytics")

@bp.route('/services')
def services():
    return render_template("services.html", title="Our Services")
