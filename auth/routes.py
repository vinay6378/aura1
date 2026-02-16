# auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timezone
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/setup-admin', methods=['GET', 'POST'])
def setup_admin():
    """One-time admin registration - only works if no admin exists"""
    # Check if admin already exists
    existing_admin = User.query.filter_by(is_admin=True).first()
    if existing_admin:
        flash('Admin account already exists. Registration is disabled.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password or not confirm_password:
            flash('All fields are required', 'error')
            return render_template('auth/setup_admin.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/setup_admin.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('auth/setup_admin.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'error')
            return render_template('auth/setup_admin.html')
        
        # Create admin user
        admin_user = User(
            username=username,
            email=email,
            is_admin=True,
            is_active=True
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        # Log in admin
        login_user(admin_user)
        
        flash('Admin account created successfully! Welcome to Aura Admin Panel.', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('auth/setup_admin.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            
            flash('Login successful!', 'success')
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('auth/login.html')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))
