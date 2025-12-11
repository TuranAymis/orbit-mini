from flask import render_template, redirect, session, url_for, request
from datetime import date
from app.main import main_bp
from app import db


@main_bp.route('/')
def index():
    """Homepage - list all events with search and filter"""
    userId = session.get('user_id')
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    # Base query for UPCOMING events
    query = """
        SELECT e.*,
               (SELECT COUNT(*) FROM event_participants WHERE event_id = e.id) AS participants,
               u.username AS creator,
               EXISTS(SELECT 1 FROM event_participants WHERE event_id = e.id AND user_id = ?) AS joined
        FROM events e
        LEFT JOIN users u ON u.id = e.user_id
        WHERE e.date >= ?
    """
    
    params = [userId, date.today()]
    
    # Add search filter
    if search_query:
        query += " AND (e.title LIKE ? OR e.description LIKE ?)"
        search_pattern = f"%{search_query}%"
        params.extend([search_pattern, search_pattern])
    
    # Add category filter
    if category_filter and category_filter != 'All':
        query += " AND e.category = ?"
        params.append(category_filter)
    
    query += " ORDER BY datetime(e.date) ASC"
    
    events = db.execute(query, *params)
    
    # Get unique categories for filter dropdown
    categories = db.execute("SELECT DISTINCT category FROM events WHERE category IS NOT NULL ORDER BY category")
    category_list = [cat['category'] for cat in categories if cat['category']]

    return render_template('index.html', events=events, categories=category_list, 
                         search_query=search_query, selected_category=category_filter)


@main_bp.route('/history')
def history():
    """Past events (History)"""
    userId = session.get('user_id')
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    # Base query for PAST events
    query = """
        SELECT e.*,
               (SELECT COUNT(*) FROM event_participants WHERE event_id = e.id) AS participants,
               u.username AS creator,
               EXISTS(SELECT 1 FROM event_participants WHERE event_id = e.id AND user_id = ?) AS joined
        FROM events e
        LEFT JOIN users u ON u.id = e.user_id
        WHERE e.date < ?
    """
    
    params = [userId, date.today()]
    
    # Add search filter
    if search_query:
        query += " AND (e.title LIKE ? OR e.description LIKE ?)"
        search_pattern = f"%{search_query}%"
        params.extend([search_pattern, search_pattern])
    
    # Add category filter
    if category_filter and category_filter != 'All':
        query += " AND e.category = ?"
        params.append(category_filter)
    
    # Sort DESCENDING by date (newest past event first)
    query += " ORDER BY datetime(e.date) DESC"
    
    events = db.execute(query, *params)
    
    # Get unique categories for filter dropdown
    categories = db.execute("SELECT DISTINCT category FROM events WHERE category IS NOT NULL ORDER BY category")
    category_list = [cat['category'] for cat in categories if cat['category']]

    return render_template('history.html', events=events, categories=category_list, 
                         search_query=search_query, selected_category=category_filter)


@main_bp.route('/profile')
def profile():
    """User profile - view created and joined events"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    userId = session['user_id']

    # Events created by the user
    my_events = db.execute("""
        SELECT e.*, e.user_id AS creator_id,
               (SELECT COUNT(*) FROM event_participants WHERE event_id = e.id) AS participants,
               u.username AS creator
        FROM events e
        LEFT JOIN users u ON u.id = e.user_id
        WHERE e.user_id = ?
        ORDER BY datetime(e.date) ASC
    """, userId)

    # Events the user has joined (created by others)
    joined = db.execute("""
        SELECT e.*, e.user_id AS creator_id,
               (SELECT COUNT(*) FROM event_participants WHERE event_id = e.id) AS participants,
               u.username AS creator
        FROM events e
        JOIN event_participants ep ON e.id = ep.event_id
        LEFT JOIN users u ON u.id = e.user_id
        WHERE ep.user_id = ?
        ORDER BY datetime(e.date) ASC
    """, userId)

    return render_template('profile.html', events=my_events, joined=joined)
