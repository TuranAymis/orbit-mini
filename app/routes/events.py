from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from app.services.event_service import EventService

events_bp = Blueprint('events', __name__, url_prefix='/events')

@events_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Create a new event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        
        if not title or not date:
            flash('Title and Date are required', 'info')
            return redirect(url_for('events.add'))

        # Create dictionary from form data
        event_data = {
            'title': title,
            'date': date,
            'time': request.form.get('time'),
            'category': request.form.get('category'),
            'description': request.form.get('description'),
            'capacity': request.form.get('capacity'),
            'location_name': request.form.get('location_name'),
            'location': request.form.get('location')
        }

        new_event, message = EventService.create_event(session['user_id'], event_data)
        
        if not new_event:
            flash(message, 'warning')
            return render_template('events/add.html'), 409

        flash(message, 'success')
        return redirect(url_for('main.index'))
    else:
        return render_template('events/add.html')


@events_bp.route('/join/<int:event_id>')
def join(event_id):
    """Join an event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    success, message = EventService.join_event(session['user_id'], event_id)
    
    if success:
        flash(message, 'success')
        return redirect(url_for('main.index'))
    else:
        flash(message, 'warning' if "full" in message or "already" in message else 'danger')
        return redirect(url_for('main.index'))


@events_bp.route('/leave/<int:event_id>')
def leave(event_id):
    """Leave an event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    success, message = EventService.leave_event(session['user_id'], event_id)
    
    if success:
        flash(message, 'danger') # Red alert for leaving is typical UI pattern here
    else:
        flash(message, 'info')
        
    return redirect(url_for('main.profile'))


@events_bp.route('/delete/<int:event_id>', methods=['POST'])
def delete(event_id):
    """Delete an event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    success, message = EventService.delete_event(session['user_id'], event_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'warning')

    return redirect(url_for('main.profile'))
