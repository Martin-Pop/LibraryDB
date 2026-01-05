import os, sys, re, json, ipaddress

class InvalidParameterException(Exception):
    pass

class ObjectAlreadyExistsException(Exception):
    pass

class DatabaseConnectionException(Exception):
    pass

def parse_db_exception(exception):
    msg = str(exception)

    if 'UNIQUE' in msg:
        pattern = r"The duplicate key value is \((.*?)\)\."
        match = re.search(pattern, msg)
        if match:
            return f"{match.group(1)} isn't unique"
        return "unique value violation"
    elif 'REFERENCE' in msg:
        return "please remove all references before proceeding"
    else:
        return msg


def get_base_paths():
    """
    Returns a dictionary with paths to key resources.

    'exe_dir': The directory where the executable (or entry script) is. Used to pathfind to configs and logs
    'data_dir': The directory where bundled resources (public/templates) live.
    :return: dictionary with log path, config folder path, public folder path
    """

    if getattr(sys, 'frozen', False): # running as an executable

        #dir where exe file is
        exe_dir = os.path.dirname(sys.executable)

        # dir where pyinstaller set code extraction (with --onedir mode its the __internal)
        data_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else exe_dir

    else:

        # main -> src -> LibraryDB
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        exe_dir = base_dir
        data_dir = base_dir

    return {
        "config_path": os.path.join(exe_dir, "config"),
        "public_path": os.path.join(data_dir, "public"),
        "log_path": os.path.join(exe_dir, "server_errors.log")
    }

def get_webserver_config(web_config_path):
    """
    Gets config file for server and validates it.
    :param web_config_path: path to config file
    :return: validated host (ip), port and secret key
    """

    if not os.path.exists(web_config_path):
        raise FileNotFoundError(f"Config error: File '{web_config_path}' was not found.")

    config_data = None
    try:
        with open(web_config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Config error: File '{web_config_path}' has invalid JSON. Details: {e}")

    required_keys = ["host", "port", "secret_key"]

    for key in required_keys:
        if key not in config_data:
            raise KeyError(f"Config error: missing key: '{key}'.")

    host = config_data["host"]
    port = config_data["port"]
    secret_key = config_data["secret_key"]

    ip_obj = ipaddress.ip_address(host)

    if not isinstance(ip_obj, ipaddress.IPv4Address):
        raise ValueError("Invalid IPv4 address.")

    if not isinstance(port, int):
        raise TypeError(f"Webserver config error: 'port' must be a number")

    if not (1 <= port <= 65535):
        raise ValueError(f"Webserver config error: 'port' must be in range from 1 to 65535. Found: {port}")

    if not isinstance(secret_key, str):
        raise TypeError(f"Webserver config error: 'secret_key' must be a string")

    return host,port,secret_key