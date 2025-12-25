from database_access.config_loader import ConfigLoader
from database_access.database_connection import DatabaseConnectionManager


if __name__ == '__main__':

    config_loader = ConfigLoader('../config/db_config.json')
    connection_string = config_loader.get_connection_string()

    db_manager = DatabaseConnectionManager(connection_string)
    db_manager.test_connection()
    try:
        print('hello')

    except Exception as e:
        print(f"Err: {e}")
    finally:
        print('closing')