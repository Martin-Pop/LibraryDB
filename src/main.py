import os

from flask import Flask, render_template
from src.controllers.author_controller import authors_bp
from src.controllers.customer_controller import customer_bp
from src.controllers.loan_controller import loan_bp
from src.controllers.title_controller import title_bp
from src.controllers.copy_controller import copy_bp
from src.utils import DatabaseConnectionException

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'public', 'templates')
static_dir = os.path.join(base_dir, 'public', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.secret_key = 'hello_world'
app.register_blueprint(authors_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(title_bp)
app.register_blueprint(copy_bp)
app.register_blueprint(loan_bp)


@app.errorhandler(DatabaseConnectionException)
def handle_db_error(e):
    return render_template('error_db.html', error=str(e)), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)