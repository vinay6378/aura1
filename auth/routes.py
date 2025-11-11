# auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db
from .forms import SecureLoginForm, SecureRegisterForm, PasswordResetRequestForm

auth_bp = Blueprint('auth', __name__)

# Password reset request route
@auth_bp.route('/password-reset-request', methods=['GET', 'POST'])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        # TODO: lookup user, generate token, send email, etc.
        flash("If an account with that email exists, you'll receive a reset link.", "info")
        return redirect(url_for('auth.login'))
    
    return render_template('auth/password_reset_request.html', form=form)

# Redirect /login to /auth/login

# Login and Register routes disabled for public website
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    flash('Login functionality is disabled. Please contact us through the contact form.', 'info')
    return redirect(url_for('main.contact'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    flash('Registration is disabled. Please contact us through the contact form.', 'info')
    return redirect(url_for('main.contact'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    from flask import Flask, redirect, url_for
