from flask import Blueprint, render_template, flash
from src.service_container import db_manager

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')


@stats_bp.route('/', methods=['GET'])
def list_stats():
    try:

        stats = db_manager.fetch_one("select * from v_stats")

        if not stats:
            flash('No statistics available yet.', 'warning')

    except Exception as e:
        stats = None
        flash(f'Error loading statistics: {str(e)}', 'error')

    return render_template('stats_page.html', stats=stats)