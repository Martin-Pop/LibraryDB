from src.database_access.config_loader import ConfigLoader
from src.database_access.database_connection import DatabaseConnectionManager
from src.models.entities import Customer, CopyStatus
from src.services.copy_service import CopyService

from src.services.customer_service import CustomerService
from src.services.author_service import AuthorService
from src.services.title_service import TitleService

from datetime import datetime
import os
if __name__ == '__main__':

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..' ,'config', 'db_config.json')

    config_loader = ConfigLoader(config_path)
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

        # author_service = AuthorService(db_manager)
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

        # title_service = TitleService(db_manager)
        #add
        # new_title = title_service.add_new_title(2,"se", None, 5, 99.50, None)
        # print('created' + repr(new_title))

        #update
        # success = title_service.update_title(5,2,"se", None, 5, 1000, None)
        # print(success)

        #delete
        # succes =  title_service.remove_title(1)
        # print(succes)

        #select
        # titles = title_service.get_titles(0,10)
        # print(titles)

        # copy_service = CopyService(db_manager)
        #add
        # copy = copy_service.add_new_copy(2, 'HHHH23', 'A2', CopyStatus.AVAILABLE)
        # print(copy)

        #update
        # success = copy_service.update_copy(5, 2, 'wow', 'A3', CopyStatus.LOST)
        # print(success)

        #delete
        # success = copy_service.remove_copy(1)
        # print(success)

        #select
        # copies = copy_service.get_copies(offset=0, limit=100)
        # for copy in copies:
        #     print(copy)
        #
        # print(copies[0].status == CopyStatus.AVAILABLE)

        #TODO: test loans
        pass

    # except Exception as e:
    #     print(f"Err: {e}")
    finally:
        print('closing')