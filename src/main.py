from database_access.config_loader import ConfigLoader
from src.database_access.database_connection import DatabaseConnectionManager
from src.models.entities import Customer

from src.services.customer_service import CustomerService

from datetime import datetime

if __name__ == '__main__':

    config_loader = ConfigLoader('../config/db_config.json')
    connection_string = config_loader.get_connection_string()

    db_manager = DatabaseConnectionManager(connection_string)
    db_manager.test_connection()

    try:

        customer_service = CustomerService(db_manager)

        new_customer = Customer(
            id=0,
            code="CUST-1s",
            first_name="j",
            last_name="n",
            email="j@n.com",
            is_active=True,
            registered_on=datetime.now()
        )

        #test
        try:
            pass
            # is_success = customer_dao.create(new_customer)
            #
            # if is_success:
            #     print("Success.")
            # else:
            #     print("No change")
            # print(cust)

            # newcust = customer_service.register_customer("Hhh", "idk", "s@sss.com")
            # cust = customer_service.get_customers(5,10)

        except Exception as e:
            print(f"Error: {e}")

    # except Exception as e:
    #     print(f"Err: {e}")
    finally:
        print('closing')