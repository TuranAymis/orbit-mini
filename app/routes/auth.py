from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username or not password or not confirmation:
            flash('All fields required', 'info')
            return redirect(url_for('auth.register'))

        if password != confirmation:
            flash('Passwords must match', 'info')
            return redirect(url_for('auth.register'))

        new_user = AuthService.register_user(username, password)
        if not new_user:
            flash('Username already exists', 'info')
            return redirect(url_for('auth.register'))

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        session.clear()

        username = request.form.get('username')
        password = request.form.get('password')

        user = AuthService.authenticate_user(username, password)
        if not user:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id
        return redirect(url_for('main.index'))
    else:
        return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('main.index'))
