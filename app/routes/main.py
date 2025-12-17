from flask import Blueprint, render_template, redirect, session, url_for, request
from app.services.event_service import EventService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage - list all events with search and filter"""
    userId = session.get('user_id')
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    events = EventService.get_upcoming_events(userId, search_query, category_filter)
    categories = EventService.get_all_categories()

    # Pre-process events to add dynamic properties like 'participants' count and 'joined' status
    # In a pure API refactor we'd serialize. Here for Jinja compatibility we pass objects
    # but we need to ensure the template can access participant counts.
    # The Model has 'participants' relationship. 
    # 'participant_names' was a specific SQL aggregate. We can replicate this logic in the template or add a property to the model.
    # For now, let's trust the model relationships in the template OR wrap them.
    # However, existing templates use dictionary access e.g., event['title'] because of cs50.
    # WE MUST CHANGE TEMPLATES TO DOT NOTATION OR WRAP.
    # STRATEGY: Update templates to use dot notation, or provide a compat layer here?
    # Refactoring to Update Templates is cleaner.

    return render_template('index.html', events=events, categories=categories, 
                         search_query=search_query, selected_category=category_filter)


@main_bp.route('/history')
def history():
    """Past events (History)"""
    userId = session.get('user_id')
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    events = EventService.get_past_events(userId, search_query, category_filter)
    categories = EventService.get_all_categories()

    return render_template('history.html', events=events, categories=categories, 
                         search_query=search_query, selected_category=category_filter)


@main_bp.route('/profile')
def profile():
    """User profile - view created and joined events"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    userId = session['user_id']

    my_events = EventService.get_user_created_events(userId)
    joined = EventService.get_user_joined_events(userId)

    return render_template('profile.html', events=my_events, joined=joined)
