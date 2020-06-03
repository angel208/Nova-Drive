import mysql.connector
import configparser



class DB_connection(object):

    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.db_config = self.config['database_dev']

        self._db_connection = None
        self._db_cur = None

    def __enter__(self):
        self._db_connection = mysql.connector.connect( host = self.db_config['host'], user = self.db_config['username'], passwd = self.db_config['password'], db = self.db_config['database'] )
        self._db_cur = self._db_connection.cursor()
        return self._db_cur

    def __del__(self):
        self._db_connection.close()