# api/routes.py
from flask import Blueprint, request, jsonify
from models import ChatbotConversation, ChatbotMessage, PageView, VisitorSession, db
from datetime import datetime, timezone
import uuid
from datetime import timedelta

api_bp = Blueprint('api', __name__)

@api_bp.route('/track/pageview', methods=['POST'])
def track_pageview():
    try:
        data = request.get_json()
        
        # Create or update visitor session
        session = VisitorSession.query.filter_by(session_id=data['session_id']).first()
        if not session:
            session = VisitorSession(
                session_id=data['session_id'],
                ip_address=request.remote_addr,
                user_agent=data.get('user_agent'),
                start_time=datetime.now(timezone.utc),
                last_activity=datetime.now(timezone.utc),
                page_views_count=1
            )
            db.session.add(session)
        else:
            session.last_activity = datetime.now(timezone.utc)
            session.page_views_count += 1
        
        # Create page view record
        page_view = PageView(
            page_url=data['page_url'],
            page_title=data.get('page_title'),
            ip_address=request.remote_addr,
            user_agent=data.get('user_agent'),
            referrer=data.get('referrer'),
            session_id=data['session_id']
        )
        
        db.session.add(page_view)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/track/event', methods=['POST'])
def track_event():
    try:
        data = request.get_json()
        # Store event data (you might want to create an Event model for this)
        # For now, just return success
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/analytics/realtime', methods=['GET'])
def realtime_analytics():
    try:
        # Get real-time statistics
        total_visitors = VisitorSession.query.count()
        total_page_views = PageView.query.count()
        active_sessions = VisitorSession.query.filter(
            VisitorSession.last_activity >= datetime.now(timezone.utc).replace(microsecond=0) - timedelta(minutes=30)
        ).count()
        
        return jsonify({
            'total_visitors': total_visitors,
            'total_page_views': total_page_views,
            'active_sessions': active_sessions,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

@api_bp.route('/chatbot/save', methods=['POST'])
def save_chatbot_conversation():
    try:
        data = request.get_json()
        
        # Create new conversation
        conversation = ChatbotConversation(
            session_id=str(uuid.uuid4()),
            user_name=data.get('name'),
            user_email=data.get('email'),
            user_phone=data.get('phone'),
            service_requested=data.get('service'),
            status='active'
        )
        
        db.session.add(conversation)
        db.session.flush()  # Get the ID without committing
        
        # Add bot messages
        bot_messages = [
            "👋 Hello! I'm Aura Assistant, your friendly AI helper!",
            f"Nice to meet you, {data.get('name')}! 🎉",
            "What's your email address?",
            "Thank you! 📧",
            "What's your contact number?",
            "Thank you! 📞",
            "What service do you need?",
            f"Perfect! I've noted that you need {data.get('service')}. ✅",
            "Thank you for providing your information! Our team will contact you soon. 🚀"
        ]
        
        user_messages = [
            data.get('name'),
            data.get('email'),
            data.get('phone'),
            data.get('service')
        ]
        
        # Add conversation messages
        message_order = [
            ('bot', bot_messages[0]),
            ('user', data.get('name')),
            ('bot', bot_messages[1]),
            ('user', data.get('email')),
            ('bot', bot_messages[2]),
            ('bot', bot_messages[3]),
            ('user', data.get('phone')),
            ('bot', bot_messages[4]),
            ('bot', bot_messages[5]),
            ('bot', bot_messages[6]),
            ('user', data.get('service')),
            ('bot', bot_messages[7]),
            ('bot', bot_messages[8])
        ]
        
        for sender, message_text in message_order:
            message = ChatbotMessage(
                conversation_id=conversation.id,
                sender=sender,
                message_text=message_text
            )
            db.session.add(message)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'conversation_id': conversation.id,
            'message': 'Conversation saved successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
