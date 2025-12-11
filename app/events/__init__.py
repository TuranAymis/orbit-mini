from flask import Blueprint

events_bp = Blueprint('events', __name__, url_prefix='/events')

from app.events import routes
