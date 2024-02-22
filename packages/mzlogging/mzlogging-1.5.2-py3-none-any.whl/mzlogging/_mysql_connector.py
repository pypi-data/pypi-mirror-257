import mysql.connector


class MySQLConnector:
    def __init__(self, credentials: dict):
        self._cnx = mysql.connector.connect(
            host=credentials.get('host'),
            user=credentials.get('user'),
            password=credentials.get('password'),
            database=credentials.get('database'),
        )
        self._cursor = self._cnx.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._cursor.close()
        self._cnx.close()

    @property
    def connection(self):
        return self._cnx

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, query, data=None, multi=False):
        try:
            self.cursor.execute(query, data, multi=multi)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def insert(self, table: str, data: dict):
        if not self.connection:
            raise mysql.connector.errors.Error("Not connected to the database.")

        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(list(data.keys()))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        values = list(data.values())

        self.execute(query, values)
        self.commit()

    # TODO: add check if table exists
    def create_table_from_schema_file(self, schema_file_path):
        with open(schema_file_path, 'r') as file:
            schema_sql = file.read()
            self.execute(schema_sql, multi=True)
            self.commit()
