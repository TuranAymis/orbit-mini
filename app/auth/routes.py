from flask import render_template, redirect, request, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import auth_bp
from app import db


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

        checkUser = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(checkUser) > 0:
            flash('Username already exists', 'info')
            return redirect(url_for('auth.register'))

        hashPassword = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashPassword)
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

        currentUser = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(currentUser) != 1 or not check_password_hash(currentUser[0]["hash"], password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        session['user_id'] = currentUser[0]['id']
        return redirect(url_for('main.index'))
    else:
        return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('main.index'))
