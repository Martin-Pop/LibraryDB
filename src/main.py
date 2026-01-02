from src.database_access.config_loader import ConfigLoader
from src.database_access.database_connection import DatabaseConnectionManager
from src.models.entities import Customer, CopyStatus
from src.services.copy_service import CopyService

from src.services.customer_service import CustomerService
from src.services.author_service import AuthorService
from src.services.loan_service import LoanService
from src.services.title_service import TitleService

from datetime import datetime
import os

from flask import Flask
from src.controllers.author_controller import authors_bp

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'public', 'templates')
static_dir = os.path.join(base_dir, 'public', 'static')

app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)

app.secret_key = 'hello_world'
app.register_blueprint(authors_bp)

@app.route('/')
def index():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)