import json
import os


class ConfigLoader:
    def __init__(self, config_path):
        self._config_path = config_path
        self._config_data = None

    def load_config(self):
        if not os.path.exists(self._config_path):
            raise FileNotFoundError(f"Config error: File '{self._config_path}' was not found.")

        try:
            with open(self._config_path, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Config error: File '{self._config_path}' has invalid JSON. Details: {e}")

        self._validate_data()
        return self._config_data

    def _validate_data(self):
        required_keys = ["driver", "server", "database", "port", "uid", "pwd"]

        for key in required_keys:
            if key not in self._config_data:
                raise KeyError(f"Config error: missing key: '{key}'.")

        driver = self._config_data["driver"]
        server = self._config_data["server"]
        database = self._config_data["database"]
        port = self._config_data["port"]
        uid = self._config_data["uid"]


        if not isinstance(driver, str) or not driver.strip():
            raise ValueError("Config error: 'driver' must be a string.")

        if not isinstance(server, str) or not server.strip():
            raise ValueError("Config error: 'server' must be a string.")

        if not isinstance(database, str) or not database.strip():
            raise ValueError("Config error: 'database' must be a string.")

        if not isinstance(uid, str) or not uid.strip():
            raise ValueError("Config error: 'uid' (username) must be a string.")

        if not isinstance(port, int):
            raise TypeError(f"Config error: 'port' must be a number")

        if not (1 <= port <= 65535):
            raise ValueError(f"Config error: 'port' must be in range from 1 to 65535. Found: {port}")

    def get_connection_string(self):
        if not self._config_data:
            self.load_config()

        #make connection string
        return (
            f"DRIVER={{{self._config_data['driver']}}};"
            f"SERVER={self._config_data['server']},{self._config_data['port']};"
            f"PORT={self._config_data['port']};"
            f"DATABASE={self._config_data['database']};"
            f"UID={self._config_data['uid']};"
            f"PWD={self._config_data['pwd']}"
        )