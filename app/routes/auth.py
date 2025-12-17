from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from app.services.auth_service import AuthService
from app.forms.auth import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = AuthService.register_user(form.username.data, form.password.data)
        if not new_user:
            flash('Username already exists', 'info')
            return redirect(url_for('auth.register'))

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    form = LoginForm()
    if form.validate_on_submit():
        session.clear()
        user = AuthService.authenticate_user(form.username.data, form.password.data)
        if not user:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id
        return redirect(url_for('main.index'))
        
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('main.index'))
