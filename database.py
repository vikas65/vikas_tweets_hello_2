from psycopg2 import pool


# static properties and methods
class Database:
    __connPool = None  # private class property

    @classmethod
    def initialise(cls , **kwargs):  # named arguments
        cls.__connPool = pool.SimpleConnectionPool(1, 50, **kwargs)  # conn object

    @classmethod
    def fetchConnection(cls):
        return cls.__connPool.getconn()

    @classmethod
    def returnConnection(cls, conn):
        cls.__connPool.putconn(conn)

    @classmethod
    def closeAll(cls):
        cls.__connPool.closeall()


class CursorFromConnectionFromPool():

    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.fetchConnection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_val, exception_tb):
        if exception_val is not None:
            self.cursor.close()
            self.connection.rollback()
            print("Exception raised !!")
        else:
            self.cursor.close()
            self.connection.commit()
        Database.returnConnection(self.connection)
