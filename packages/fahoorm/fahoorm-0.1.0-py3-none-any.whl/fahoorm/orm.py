import sqlite3
import psycopg2
import pymysql
import pymongo
from typing import Union

class Entity:
    def __init__(self):
        self._id = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

class Session:
    def __init__(self, database_url: str):
        self.connection = None
        self.cursor = None
        self._connect(database_url)

    def _connect(self, database_url: str):
        if database_url.startswith('sqlite://'):
            self.connection = sqlite3.connect(database_url.replace('sqlite://', ''))
            self.cursor = self.connection.cursor()
        elif database_url.startswith('postgresql://'):
            conn_str = database_url.replace('postgresql://', '')
            self.connection = psycopg2.connect(conn_str)
            self.cursor = self.connection.cursor()
        elif database_url.startswith('mysql://'):
            conn_str = database_url.replace('mysql://', '')
            self.connection = pymysql.connect(*conn_str.split('/'), autocommit=True)
            self.cursor = self.connection.cursor()
        elif database_url.startswith('mongodb://'):
            self.connection = pymongo.MongoClient(database_url)
            self.cursor = None  # MongoDB does not use cursors

    def execute(self, query: str):
        if self.cursor:
            self.cursor.execute(query)
        else:
            raise NotImplementedError("MongoDB does not support execute method")

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
