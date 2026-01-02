from src.database_access.database_connection import DatabaseConnectionManager
from src.database_access.config_loader import ConfigLoader
from src.services.author_service import AuthorService
from src.services.customer_service import CustomerService
from src.services.loan_service import LoanService

import os

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..' ,'config', 'db_config.json')

config_loader = ConfigLoader(config_path)
connection_string = config_loader.get_connection_string()

db_manager = DatabaseConnectionManager(connection_string)
# db_manager.test_connection()

#SERVICES
author_service = AuthorService(db_manager)
customer_service = CustomerService(db_manager)
loan_service = LoanService(db_manager)
