from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from app.services.event_service import EventService

events_bp = Blueprint('events', __name__, url_prefix='/events')

from app.forms.event import EventForm, CommentForm

@events_bp.route('/add', methods=['GET', 'POST'])
def add():
    """Create a new event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    form = EventForm()
    if form.validate_on_submit():
        event_data = {
            'title': form.title.data,
            'date': str(form.date.data), # Convert date object to string for DB
            'time': str(form.time.data) if form.time.data else None,
            'category': form.category.data,
            'description': form.description.data,
            'capacity': form.capacity.data,
            'location_name': form.location_name.data,
            'location': form.location.data,
            'image_url': form.image_url.data
        }

        new_event, message = EventService.create_event(session['user_id'], event_data)
        
        if not new_event:
            flash(message, 'warning')
            return render_template('events/add.html', form=form), 409

        flash(message, 'success')
        return redirect(url_for('main.index'))
        
    return render_template('events/add.html', form=form)


@events_bp.route('/detail/<int:event_id>', methods=['GET', 'POST'])
def detail(event_id):
    """Event detail view with comments"""
    event = EventService.get_event_with_details(event_id)
    if not event:
        flash('Event not found', 'danger')
        return redirect(url_for('main.index'))

    is_modal = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Comment handling
    form = CommentForm()
    if 'user_id' in session and form.validate_on_submit():
        new_comment, msg = EventService.add_comment(session['user_id'], event_id, form.content.data)
        if new_comment:
            flash(msg, 'success')
        else:
            flash(msg, 'warning')
            
        # If AJAX, return the updated partial for the modal
        if is_modal:
            comments = EventService.get_comments(event_id)
            return render_template('events/_detail_content.html', event=event, comments=comments, form=form, is_modal=True)

        return redirect(url_for('events.detail', event_id=event_id))

    comments = EventService.get_comments(event_id)
    
    if is_modal:
        return render_template('events/_detail_content.html', event=event, comments=comments, form=form, is_modal=True)
    
    return render_template('events/detail.html', event=event, comments=comments, form=form)


@events_bp.route('/join/<int:event_id>')
def join(event_id):
    """Join an event"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    success, message = EventService.join_event(session['user_id'], event_id)
    
    # Handle AJAX request (from Modal)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        flash(message, 'success' if success else 'warning')
        # Re-fetch data for the partial
        event = EventService.get_event_with_details(event_id)
        comments = EventService.get_comments(event_id)
        from app.forms.event import CommentForm
        form = CommentForm()
        return render_template('events/_detail_content.html', event=event, comments=comments, form=form, is_modal=True)

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
    
    # Handle AJAX request (from Modal)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        flash(message, 'success' if success else 'warning')
        # Re-fetch data for the partial
        event = EventService.get_event_with_details(event_id)
        comments = EventService.get_comments(event_id)
        from app.forms.event import CommentForm
        form = CommentForm()
        return render_template('events/_detail_content.html', event=event, comments=comments, form=form, is_modal=True)

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
