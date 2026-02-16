# admin/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import User, ContactMessage, ChatbotConversation, ChatbotMessage, PageView, VisitorSession, db
from datetime import datetime, timezone

admin_bp = Blueprint('admin', __name__)

# Admin access control
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with overview stats"""
    # Get statistics
    total_contacts = ContactMessage.query.count()
    unread_contacts = ContactMessage.query.filter_by(is_read=False).count()
    total_chatbot_conversations = ChatbotConversation.query.count()
    active_chatbot_conversations = ChatbotConversation.query.filter_by(status='active').count()
    total_page_views = PageView.query.count()
    total_sessions = VisitorSession.query.count()
    
    # Get message counts for template
    total_messages = ContactMessage.query.count()
    new_messages = ContactMessage.query.filter_by(status='new').count()
    pending_messages = ContactMessage.query.filter_by(status='pending').count()
    responded_messages = ContactMessage.query.filter_by(status='responded').count()
    closed_messages = ContactMessage.query.filter_by(status='closed').count()
    
    # Get recent activities
    recent_contacts = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    recent_chatbot = ChatbotConversation.query.order_by(ChatbotConversation.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_contacts=total_contacts,
                         unread_contacts=unread_contacts,
                         total_chatbot_conversations=total_chatbot_conversations,
                         active_chatbot_conversations=active_chatbot_conversations,
                         total_page_views=total_page_views,
                         total_sessions=total_sessions,
                         recent_contacts=recent_contacts,
                         recent_chatbot=recent_chatbot,
                         total_messages=total_messages,
                         new_messages=new_messages,
                         pending_messages=pending_messages,
                         responded_messages=responded_messages,
                         closed_messages=closed_messages)

@admin_bp.route('/messages')
@login_required
@admin_required
def messages():
    """Manage contact messages"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = ContactMessage.query
    
    # Get counts for template
    total_messages = ContactMessage.query.count()
    new_messages = ContactMessage.query.filter_by(status='new').count()
    pending_messages = ContactMessage.query.filter_by(status='pending').count()
    responded_messages = ContactMessage.query.filter_by(status='responded').count()
    closed_messages = ContactMessage.query.filter_by(status='closed').count()
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    messages = query.order_by(ContactMessage.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/messages.html', 
                         messages=messages, 
                         status=status,
                         total_messages=total_messages,
                         new_messages=new_messages,
                         pending_messages=pending_messages,
                         responded_messages=responded_messages,
                         closed_messages=closed_messages)

@admin_bp.route('/messages/<int:message_id>')
@login_required
@admin_required
def view_message(message_id):
    """View individual message"""
    message = ContactMessage.query.get_or_404(message_id)
    
    # Mark as read
    if not message.is_read:
        message.is_read = True
        message.read_at = datetime.now(timezone.utc)
        db.session.commit()
    
    return render_template('admin/view_message.html', message=message)

@admin_bp.route('/messages/<int:message_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_message(message_id):
    """Delete message"""
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    
    flash('Message deleted successfully.', 'success')
    return redirect(url_for('admin.messages'))

@admin_bp.route('/messages/<int:message_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_message_status(message_id):
    """Toggle message status"""
    message = ContactMessage.query.get_or_404(message_id)
    
    status_cycle = ['new', 'pending', 'responded', 'closed']
    current_index = status_cycle.index(message.status) if message.status in status_cycle else 0
    next_index = (current_index + 1) % len(status_cycle)
    message.status = status_cycle[next_index]
    
    db.session.commit()
    
    return jsonify({'status': message.status})

@admin_bp.route('/chatbot')
@login_required
@admin_required
def chatbot():
    """Manage chatbot conversations"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = ChatbotConversation.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    # Get counts for template
    total_conversations = ChatbotConversation.query.count()
    active_conversations = ChatbotConversation.query.filter_by(status='active').count()
    completed_conversations = ChatbotConversation.query.filter_by(status='completed').count()
    follow_up_conversations = ChatbotConversation.query.filter_by(status='follow_up').count()
    
    conversations = query.order_by(ChatbotConversation.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/chatbot.html', 
                         conversations=conversations, 
                         status=status,
                         total_conversations=total_conversations,
                         active_conversations=active_conversations,
                         completed_conversations=completed_conversations,
                         follow_up_conversations=follow_up_conversations)

@admin_bp.route('/chatbot/<int:conversation_id>')
@login_required
@admin_required
def view_conversation(conversation_id):
    """View individual chatbot conversation"""
    conversation = ChatbotConversation.query.get_or_404(conversation_id)
    messages = ChatbotMessage.query.filter_by(conversation_id=conversation_id).order_by(ChatbotMessage.created_at).all()
    
    return render_template('admin/view_conversation.html', conversation=conversation, messages=messages)

@admin_bp.route('/chatbot/<int:conversation_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_conversation(conversation_id):
    """Delete chatbot conversation"""
    conversation = ChatbotConversation.query.get_or_404(conversation_id)
    db.session.delete(conversation)
    db.session.commit()
    
    flash('Conversation deleted successfully.', 'success')
    return redirect(url_for('admin.chatbot'))

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """Website analytics"""
    # Get page view statistics
    total_page_views = PageView.query.count()
    unique_sessions = VisitorSession.query.count()
    
    # Get recent page views
    recent_views = PageView.query.order_by(PageView.created_at.desc()).limit(100).all()
    
    # Get top pages
    top_pages = db.session.query(
        PageView.page_url, 
        db.func.count(PageView.id).label('views')
    ).group_by(PageView.page_url).order_by(db.func.count(PageView.id).desc()).limit(10).all()
    
    return render_template('admin/analytics.html', 
                         total_page_views=total_page_views,
                         unique_sessions=unique_sessions,
                         recent_views=recent_views,
                         top_pages=top_pages)

@admin_bp.route('/profile')
@login_required
@admin_required
def profile():
    """Admin profile settings"""
    return render_template('admin/profile.html')

@admin_bp.route('/profile/update', methods=['POST'])
@login_required
@admin_required
def update_profile():
    """Update admin profile"""
    username = request.form.get('username')
    email = request.form.get('email')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    if not username or not email:
        flash('Username and email are required.', 'error')
        return redirect(url_for('admin.profile'))
    
    # Check if email is being changed and if it's already taken
    if email != current_user.email:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', 'error')
            return redirect(url_for('admin.profile'))
    
    # Update user info
    current_user.username = username
    current_user.email = email
    
    # Update password if provided
    if new_password:
        if not current_password or not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('admin.profile'))
        
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long.', 'error')
            return redirect(url_for('admin.profile'))
        
        current_user.set_password(new_password)
        flash('Password updated successfully.', 'success')
    
    db.session.commit()
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('admin.profile'))
