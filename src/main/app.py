import os, logging

from flask import Flask, render_template
from src.controllers.author_controller import authors_bp
from src.controllers.customer_controller import customer_bp
from src.controllers.loan_controller import loan_bp
from src.controllers.stats_controller import stats_bp
from src.controllers.title_controller import title_bp
from src.controllers.copy_controller import copy_bp
from src.main.utils import DatabaseConnectionException

from src.main.utils import get_base_paths, get_webserver_config

paths = get_base_paths()

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

    logging.basicConfig(
        filename=paths['log_path'],
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    logging.getLogger().addHandler(console_handler)

    try:
        valid_host, valid_port, valid_secret_key = get_webserver_config(web_config_path)
        app.secret_key = valid_secret_key

        app.run(host=valid_host, port=valid_port,debug=False)
        print(f"Server started at {valid_host}:{valid_port}")
    except Exception as e:
        logging.error(f"Error: {e}")