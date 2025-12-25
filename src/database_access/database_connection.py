import pyodbc


class DatabaseConnectionManager:
    _instance = None
    _connection = None
    _connection_string = None

    def __new__(cls, connection_string=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # first instantiation must specify connection string
            if connection_string is None:
                raise ValueError("Connection string must be entered before creating Singleton instance.")

            cls._instance._connection_string = connection_string
        return cls._instance

    def _establish_connection(self):

        if self._connection is None: #lazy
            if self._connection_string is None:
                raise Exception("Can not connect, connection string doesnt exist.")

            try:
                self._connection = pyodbc.connect(self._connection_string)
            except pyodbc.Error as ex:
                raise Exception(f"Error connecting to db: {ex}")

    def get_connection(self):
        self._establish_connection()
        return self._connection

    def fetch_all(self, query, params=None):
        self._establish_connection()
        cursor = self._connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return results
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        self._establish_connection()
        cursor = self._connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
        finally:
            cursor.close()

    def execute(self, query, params=None, auto_commit=True):
        self._establish_connection()
        cursor = self._connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            rows_affected = cursor.rowcount

            if auto_commit:
                self._connection.commit()

            return rows_affected
        except pyodbc.Error:
            self._connection.rollback()
            raise
        finally:
            cursor.close()

    def begin_transaction(self):
        self._establish_connection()
        self._connection.autocommit = False

    def commit(self):
        if self._connection:
            self._connection.commit()

    def rollback(self):
        if self._connection:
            self._connection.rollback()

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def test_connection(self):
        self._establish_connection()