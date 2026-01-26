# admin/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from functools import wraps
from models import User, ContactMessage, ChatbotConversation, ChatbotMessage
from extensions import db
from datetime import datetime, timezone, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv
import io

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login')
def login():
    return redirect(url_for('auth.login'))

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get real-time statistics
    total_messages = ContactMessage.query.count()
    total_chats = ChatbotConversation.query.count()
    total_users = User.query.count()
    
    # Get recent messages with priority
    recent_messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).limit(5).all()
    
    # Get recent chats
    recent_chats = ChatbotConversation.query.order_by(
        ChatbotConversation.created_at.desc()
    ).limit(3).all()
    
    # Load messages for chats
    for chat in recent_chats:
        chat.messages = ChatbotMessage.query.filter_by(
            conversation_id=chat.id
        ).order_by(ChatbotMessage.created_at.asc()).all()
    
    return render_template('admin/dashboard.html',
                         total_messages=total_messages,
                         total_chats=total_chats,
                         total_users=total_users,
                         unread_messages=get_unread_count(),
                         today_messages=get_today_messages(),
                         today_chats=get_today_chats(),
                         active_users=get_active_users(),
                         new_users_today=get_new_users_today(),
                         total_page_views=get_total_page_views(),
                         today_page_views=get_today_page_views(),
                         unique_visitors_today=get_unique_visitors_today(),
                         active_chats=get_active_chats(),
                         recent_messages=recent_messages,
                         recent_chats=recent_chats)

def get_unread_count():
    """Count unread messages"""
    return ContactMessage.query.filter_by(is_read=False).count()

def get_today_messages():
    """Count messages received today"""
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return ContactMessage.query.filter(ContactMessage.created_at >= today).count()

def get_today_chats():
    """Count chats created today"""
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return ChatbotConversation.query.filter(ChatbotConversation.created_at >= today).count()

def get_active_users():
    """Count users who logged in the last 30 days"""
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    return User.query.filter(User.last_login >= thirty_days_ago).count()

def get_new_users_today():
    """Count new users who registered today"""
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return User.query.filter(User.created_at >= today).count()

def get_total_page_views():
    """Get total page views (simplified)"""
    return 1000  # Placeholder - implement actual page tracking

def get_today_page_views():
    """Get today's page views"""
    return 250  # Placeholder - implement actual page tracking

def get_unique_visitors_today():
    """Get today's unique visitors"""
    return 120  # Placeholder - implement actual visitor tracking

def get_active_chats():
    """Count chats with activity in the last hour"""
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    return ChatbotConversation.query.filter(
        ChatbotConversation.last_activity >= one_hour_ago
    ).count()

# Message routes
@admin_bp.route('/messages')
@login_required
@admin_required
def messages():
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/messages.html', messages=messages)

@admin_bp.route('/message/<int:message_id>')
@login_required
@admin_required
def message_detail(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    
    # Mark as read if not already read
    if not message.is_read:
        message.is_read = True
        message.read_at = datetime.now(timezone.utc)
        db.session.commit()
    
    return render_template('admin/message_detail.html', message=message)

@admin_bp.route('/message/<int:message_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin.messages'))

@admin_bp.route('/message/<int:message_id>/archive', methods=['POST'])
@login_required
@admin_required
def archive_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    message.is_archived = True
    db.session.commit()
    return jsonify({'success': True})

@admin_bp.route('/message/<int:message_id>/read', methods=['POST'])
@login_required
@admin_required
def mark_message_read(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = True
    message.read_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify({'success': True})

@admin_bp.route('/messages/mark-all-read', methods=['POST'])
@login_required
@admin_required
def mark_all_read():
    ContactMessage.query.filter_by(is_read=False).update({
        'is_read': True,
        'read_at': datetime.now(timezone.utc)
    })
    db.session.commit()
    return jsonify({'success': True})

@admin_bp.route('/messages/export')
@login_required
@admin_required
def export_messages():
    def generate_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Name', 'Email', 'Phone', 'Subject', 'Message', 'Status', 'Priority', 'Created At'])
        
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        for message in messages:
            writer.writerow([
                message.name,
                message.email,
                message.phone or '',
                message.subject,
                message.message,
                message.status,
                message.priority,
                message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        output.seek(0)
        return output.getvalue()
    
    output = generate_csv()
    return send_file(
        io.BytesIO(output.encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'messages_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@admin_bp.route('/send-reply', methods=['POST'])
@login_required
@admin_required
def send_reply():
    data = request.get_json()
    
    try:
        # Send email reply
        msg = MIMEMultipart()
        msg['From'] = os.environ.get('MAIL_USERNAME', 'gautamvinay939@gmail.com')
        msg['To'] = data['to']
        msg['Subject'] = data['subject']
        
        # Create email body
        body = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h2 style="color: white; margin: 0;">Aura - Response to Your Inquiry</h2>
                </div>
                <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px;">
                    <p>Dear Customer,</p>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        {data['message'].replace('\n', '<br>')}
                    </div>
                    <p>Best regards,<br>Aura Team</p>
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
            smtp_server.login(os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD'))
            smtp_server.send_message(msg)
            smtp_server.quit()
            
            # Send copy if requested
            if data.get('send_copy'):
                msg['To'] = os.environ.get('MAIL_USERNAME')
                msg['Subject'] = f"Copy: {data['subject']}"
                smtp_server.send_message(msg)
            
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Email not configured'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Chatbot routes
@admin_bp.route('/chatbot')
@login_required
@admin_required
def chatbot():
    conversations = ChatbotConversation.query.order_by(
        ChatbotConversation.created_at.desc()
    ).all()
    
    # Load messages for each conversation
    for conv in conversations:
        conv.messages = ChatbotMessage.query.filter_by(
            conversation_id=conv.id
        ).order_by(ChatbotMessage.created_at.asc()).all()
    
    return render_template('admin/chatbot.html', conversations=conversations)

@admin_bp.route('/chat/<int:chat_id>')
@login_required
@admin_required
def chat_detail(chat_id):
    conversation = ChatbotConversation.query.get_or_404(chat_id)
    
    messages = ChatbotMessage.query.filter_by(
        conversation_id=chat_id
    ).order_by(ChatbotMessage.created_at.asc()).all()
    
    return jsonify({
        'id': conversation.id,
        'user_name': conversation.user_name,
        'user_email': conversation.user_email,
        'user_phone': conversation.user_phone,
        'service_requested': conversation.service_requested,
        'status': conversation.status,
        'created_at': conversation.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'messages': [{
            'sender': msg.sender,
            'message_text': msg.message_text,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for msg in messages]
    })

@admin_bp.route('/chat/<int:chat_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_chat(chat_id):
    conversation = ChatbotConversation.query.get_or_404(chat_id)
    
    # Delete all associated messages
    ChatbotMessage.query.filter_by(
        conversation_id=chat_id
    ).delete()
    
    db.session.delete(conversation)
    db.session.commit()
    return jsonify({'success': True})

@admin_bp.route('/chat/<int:chat_id>/archive', methods=['POST'])
@login_required
@admin_required
def archive_chat(chat_id):
    conversation = ChatbotConversation.query.get_or_404(chat_id)
    conversation.status = 'archived'
    db.session.commit()
    return jsonify({'success': True})

@admin_bp.route('/chats/export')
@login_required
@admin_required
def export_chats():
    def generate_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['User Name', 'Email', 'Phone', 'Service Requested', 'Status', 'Created At'])
        
        conversations = ChatbotConversation.query.order_by(
            ChatbotConversation.created_at.desc()
        ).all()
        for conv in conversations:
            writer.writerow([
                conv.user_name or 'Anonymous',
                conv.user_email or '',
                conv.user_phone or '',
                conv.service_requested or 'General',
                conv.status,
                conv.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        output.seek(0)
        return output.getvalue()
    
    output = generate_csv()
    return send_file(
        io.BytesIO(output.encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'chats_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

# Profile route
@admin_bp.route('/profile')
@login_required
@admin_required
def profile():
    return render_template('admin/profile.html')

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    # Simple analytics page
    analytics_data = {
        'total_visitors': 1250,
        'total_page_views': 5432,
        'avg_time_on_site': 4.5,
        'bounce_rate': 32.5,
        'daily_visitors': [120, 145, 130, 165, 180, 155, 190],
        'page_views': [450, 520, 480, 590, 610, 540, 680],
        'top_pages': [
            {'page': '/', 'views': 1250, 'percentage': 23.0},
            {'page': '/contact', 'views': 432, 'percentage': 8.0},
            {'page': '/about', 'views': 298, 'percentage': 5.5},
            {'page': '/events', 'views': 187, 'percentage': 3.4},
        ]
    }
    
    return render_template('admin/analytics.html', analytics=analytics_data)

@admin_bp.route('/profile', methods=['POST'])
@login_required
@admin_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Update username and email
    if username and username != current_user.username:
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Username already exists!', 'error')
            return redirect(url_for('admin.profile'))
        current_user.username = username
    
    if email and email != current_user.email:
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Email already exists!', 'error')
            return redirect(url_for('admin.profile'))
        current_user.email = email
    
    # Update password if provided
    if current_password and new_password:
        if not current_user.check_password(current_password):
            flash('Current password is incorrect!', 'error')
            return redirect(url_for('admin.profile'))
        
        if new_password != confirm_password:
            flash('New passwords do not match!', 'error')
            return redirect(url_for('admin.profile'))
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return redirect(url_for('admin.profile'))
        
        current_user.set_password(new_password)
        flash('Password updated successfully!', 'success')
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('admin.profile'))
