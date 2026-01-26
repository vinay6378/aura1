# auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from extensions import db
import secrets
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('admin/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('admin/login.html')
    
    return render_template('admin/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('auth/simple_register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'error')
            return render_template('auth/simple_register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            is_admin=True,  # Make first user admin
            is_active=True
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/simple_register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Email is required', 'error')
            return render_template('auth/forgot_password.html')
        
        user = User.query.filter_by(email=email, is_admin=True).first()
        
        if user:
            if user.security_key:
                flash('A security key has already been set for this account. Please use the security key to reset your password.', 'info')
                return redirect(url_for('auth.verify_security_key'))
            else:
                flash('No security key found for this account. Please contact the system administrator.', 'error')
        else:
            flash('If an admin account with this email exists, you will receive instructions to set up a security key.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')

@auth_bp.route('/setup-security-key', methods=['GET', 'POST'])
def setup_security_key():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Email is required', 'error')
            return render_template('auth/setup_security_key.html')
        
        user = User.query.filter_by(email=email, is_admin=True).first()
        
        if user and not user.security_key:
            # Generate a unique security key
            security_key = secrets.token_urlsafe(32)
            user.security_key = security_key
            db.session.commit()
            
            flash(f'Security key generated: {security_key}', 'success')
            flash('Please save this security key in a secure location. You will need it to reset your password.', 'warning')
            return redirect(url_for('auth.login'))
        elif user and user.security_key:
            flash('Security key already exists for this account.', 'error')
        else:
            flash('Admin account not found.', 'error')
    
    return render_template('auth/setup_security_key.html')

@auth_bp.route('/verify-security-key', methods=['GET', 'POST'])
def verify_security_key():
    if request.method == 'POST':
        email = request.form.get('email')
        security_key = request.form.get('security_key')
        
        if not email or not security_key:
            flash('Email and security key are required', 'error')
            return render_template('auth/verify_security_key.html')
        
        user = User.query.filter_by(email=email, is_admin=True).first()
        
        if user and user.security_key == security_key:
            session['reset_user_id'] = user.id
            flash('Security key verified! You can now reset your password.', 'success')
            return redirect(url_for('auth.reset_password'))
        else:
            flash('Invalid email or security key', 'error')
    
    return render_template('auth/verify_security_key.html')

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_user_id' not in session:
        flash('Please verify your security key first', 'error')
        return redirect(url_for('auth.verify_security_key'))
    
    user = User.query.get(session['reset_user_id'])
    
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not new_password or not confirm_password:
            flash('Both password fields are required', 'error')
            return render_template('auth/reset_password.html')
        
        if new_password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/reset_password.html')
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('auth/reset_password.html')
        
        user.set_password(new_password)
        db.session.commit()
        
        # Clear the session
        session.pop('reset_user_id', None)
        
        flash('Password reset successfully! You can now login with your new password.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html')
