import os, logging
import sys

from src.main.utils import get_base_paths

paths = get_base_paths()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(paths['log_path'])
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

from flask import Flask, render_template
from src.controllers.author_controller import authors_bp
from src.controllers.customer_controller import customer_bp
from src.controllers.loan_controller import loan_bp
from src.controllers.stats_controller import stats_bp
from src.controllers.title_controller import title_bp
from src.controllers.copy_controller import copy_bp
from src.main.utils import DatabaseConnectionException
from src.main.utils import get_webserver_config
from src.main.service_container import db_manager

template_folder = os.path.join(paths['public_path'], 'templates')
static_folder = os.path.join(paths['public_path'], 'static')
web_config_path = os.path.join(paths['config_path'], 'webserver_config.json')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.register_blueprint(authors_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(title_bp)
app.register_blueprint(copy_bp)
app.register_blueprint(loan_bp)
app.register_blueprint(stats_bp)


@app.errorhandler(DatabaseConnectionException)
def handle_db_error(e):
    return render_template('error_db.html', error=str(e)), 500

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)

    try:
        valid_host, valid_port, valid_secret_key = get_webserver_config(web_config_path)
        app.secret_key = valid_secret_key

        logger.info(f" Server listening on {valid_host}:{valid_port}")
        app.run(host=valid_host, port=valid_port,debug=False)
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if db_manager:
            db_manager.close_connection()