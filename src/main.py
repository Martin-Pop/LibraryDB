from database_access.config_loader import ConfigLoader
from src.database_access.database_connection import DatabaseConnectionManager
from src.models.entities import Customer

from src.services.customer_service import CustomerService
from src.services.author_service import AuthorService

from datetime import datetime

if __name__ == '__main__':

    config_loader = ConfigLoader('../config/db_config.json')
    connection_string = config_loader.get_connection_string()

    db_manager = DatabaseConnectionManager(connection_string)
    db_manager.test_connection()

    try:

        #customer_service = CustomerService(db_manager)
        #add
        # new_customer = customer_service.register_customer("Martin", "idk", "s@sss.com")
        # print('New customer:' + repr(new_customer))

        #update
        # success = customer_service.update_customer(4, "Martin", "Pp", "s@.com")
        # print(success)

        # select with offset, limit
        # cust = customer_service.get_customers(0,10)
        # print(cust)

        #remove
        # success = customer_service.remove_customer(3)
        # print(f"Removed customer: {success}")

        author_service = AuthorService(db_manager)
        #add
        # new_author = author_service.add_new_author("John", "Doe", "USA")
        # print("new author:" + repr(new_author))

        #update
        # success = author_service.update_author(2,"Johnny", "Doe", "UK")
        # print(success)

        #delete
        # success = author_service.remove_author(1)
        # print(success)

        #select
        # auths = author_service.get_authors(0,10)
        # print(auths)

    except Exception as e:
        print(f"Err: {e}")
    finally:
        print('closing')