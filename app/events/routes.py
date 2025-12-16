from flask import render_template, redirect, request, session, flash, url_for
from app.events import events_bp
from app import db


@events_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Create a new event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        time = request.form.get('time')
        category = request.form.get('category')
        description = request.form.get('description')
        capacity = request.form.get('capacity')
        location_name = request.form.get('location_name')
        location = request.form.get('location')

        if not title or not date:
            flash('Title and Date are required', 'info')
            return redirect(url_for('events.add'))

        # Empty capacity is considered unlimited
        if not capacity:
            capacity = None
        
        if not category:
            category = 'General'

        # Spam Protection: Check for duplicates
        existing_event = db.execute(
            "SELECT id FROM events WHERE user_id = ? AND title = ? AND date = ?", 
            session['user_id'], title, date
        )
        
        if existing_event:
            flash('This event already exists.', 'warning')
            return render_template('events/add.html'), 409

        db.execute("""
            INSERT INTO events (user_id, title, date, time, category, description, capacity, location, location_name, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, session['user_id'], title, date, time, category, description, capacity, location, location_name)

        flash('Event added successfully!', 'success')
        return redirect(url_for('main.index'))
    else:
        return render_template('events/add.html')


@events_bp.route('/join/<int:event_id>')
def join(event_id):
    """Join an event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    userId = session['user_id']

    # Get event information
    event = db.execute("SELECT capacity FROM events WHERE id = ?", event_id)
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('main.index'))

    capacity = event[0]['capacity']
    count = db.execute(
        "SELECT COUNT(*) AS total FROM event_participants WHERE event_id = ?", event_id)[0]['total']

    # If the capacity is full
    if capacity and count >= capacity:
        flash('Event is full.', 'warning')
        return redirect(url_for('main.index'))

    # Already joined?
    existing = db.execute(
        "SELECT * FROM event_participants WHERE user_id = ? AND event_id = ?", userId, event_id)
    if existing:
        flash('You already joined this event.', 'info')
        return redirect(url_for('main.index'))

    # Joining action
    db.execute("INSERT INTO event_participants (user_id, event_id) VALUES (?, ?)", userId, event_id)
    flash('You have joined the event!', 'success')
    return redirect(url_for('main.index'))


@events_bp.route('/leave/<int:event_id>')
def leave(event_id):
    """Leave an event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    userId = session['user_id']

    # Check if joined
    existing = db.execute(
        "SELECT * FROM event_participants WHERE user_id = ? AND event_id = ?", userId, event_id)
    if not existing:
        flash('You are not part of this event.', 'info')
        return redirect(url_for('main.profile'))

    db.execute("DELETE FROM event_participants WHERE user_id = ? AND event_id = ?", userId, event_id)
    flash('You have left the event.', 'danger')
    return redirect(url_for('main.profile'))


@events_bp.route('/delete/<int:event_id>', methods=['POST'])
def delete(event_id):
    """Delete an event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    userId = session['user_id']

    # Check if the event really belongs to this user
    event = db.execute("SELECT * FROM events WHERE id = ? AND user_id = ?", event_id, userId)
    if not event:
        flash('You can only delete your own events.', 'warning')
        return redirect(url_for('main.profile'))

    # Also delete participation records
    db.execute("DELETE FROM event_participants WHERE event_id = ?", event_id)

    # Delete the event
    db.execute("DELETE FROM events WHERE id = ? AND user_id = ?", event_id, userId)

    flash('Event deleted successfully!', 'success')
    return redirect(url_for('main.profile'))
