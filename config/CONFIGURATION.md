# Database and webserver configuration
Configure configuration files for webserver and database connection.

## 1. Configure webserver

1.  Navigate to `config/webserver_config.json` and open it.
2.  Change the following parameters according to your environment:
    -   **`host`**: Set the IP address where the Flask application will listen. Use `127.0.0.1` for local testing or `0.0.0.0` to allow access from other devices in the network.
    -   **`port`**: The network port on which the server runs (default is `8080`). Ensure this port is not being used by another application and is allowed in your firewall settings.
    -   **`secret_key`**: A unique string used to secure session cookies and sign data. (Needed for Flask flashed messages)

## 2. Configure database connection
1.  Navigate to `config/db_config.json` and open it.
2.  Update the fields to match your local SQL Server setup:
    -   **`driver`**: The specific ODBC driver installed on your system ( `'ODBC Driver 17 for SQL Server'`). Ensure this driver is downloaded and installed from Microsoft's website.
    -   **`server`**: The address of your SQL Server instance.
        -   If you want to specify port use format `127.0.0.1,1433` .
        -   If you use a **Named Instance**, use the format `localhost\InstanceName`.
    -   **`database`**: The name of the specific database you created ( `'my_library'`).
    -   **`uid`**: The SQL Server Login created for the application ( `'library_user'`). 
    -   **`pwd`**: The password associated with the SQL Login.