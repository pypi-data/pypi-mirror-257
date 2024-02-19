import mysql.connector

class Database:
    def __init__(self, endpoint, database_name, username, password):
        self.database = None
        self.cursor = None
        self.data = [endpoint, database_name, username, password]
        self.database_name = database_name

    def connect(self):
        self.database = mysql.connector.connect(host=self.data[0], user=self.data[2], password=self.data[3], database=self.data[1])
        self.cursor = self.database.cursor()

    def disconnect(self, commit=False):
        if commit is True:
            self.database.commit()
        self.cursor.close()
        self.database.close()

    def add(self, table_name, columns, values: list):
        self.connect()
        values = ", ".join(f'"{value}"' for value in values)
        self.cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({values});')
        self.disconnect(commit=True)

    def get(self, table_name, columns, where=None, fetchall=False):
        self.connect()
        if where is None:
            self.cursor.execute(f'SELECT {columns} FROM {self.database_name}.{table_name};')
        else:
            self.cursor.execute(f'SELECT {columns} FROM {self.database_name}.{table_name} WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
        result = self.cursor.fetchall()
        self.disconnect()
        if fetchall is False:
            return result[0]
        else:
            return result

    def delete(self, table_name, colum=None, where=None):
        self.connect()
        if where is None:
            if colum is None:
                self.cursor.execute(f'DELETE FROM {self.database_name}.{table_name};')
            else:
                self.cursor.execute(f'DELETE {colum} FROM {self.database_name}.{table_name};')
        else:
            if colum is None:
                self.cursor.execute(f'DELETE FROM {self.database_name}.{table_name} WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
            else:
                self.cursor.execute(f'DELETE {colum} FROM {self.database_name}.{table_name} WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
        self.disconnect(commit=True)

    def edit(self, table_name, column, value, where=None):
        self.connect()
        if where is None:
            self.cursor.execute(f'UPDATE {self.database_name}.{table_name} SET {column} = "{value}";')
        else:
            self.cursor.execute(f'UPDATE {self.database_name}.{table_name} SET {column} = "{value}" WHERE {where.split(" = ")[0]} = "{where.split(" = ")[1]}";')
        self.disconnect(commit=True)

    def default(self, table_name, columns: list):
        self.connect()
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.database_name}.{table_name} ({", ".join(columns)});')
        self.disconnect(commit=True)
