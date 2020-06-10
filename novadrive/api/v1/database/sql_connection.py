import mysql.connector
import configparser, os

class DBConnection(object):

    def __init__(self, testing = False ):

        #get environment
        try:
            self.env = os.environ['NOVA_ENV'] 
        except KeyError:  
            os.environ['NOVA_ENV'] = 'DEV'
            self.env = os.environ['NOVA_ENV'] 
        
        print ( "db connection environment: " + self.env)

        #get config file
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        #set config data based on environment
        if( testing == True or self.env == 'TEST' ):
            self.db_config = self.config['database_test']
        elif ( self.env == 'PROD' ):
            self.db_config = self.config['database_prod']
        else:
            self.db_config = self.config['database_dev']

        self._db_connection = None
        self._db_cur = None 

    def __enter__(self):
        self._db_connection = mysql.connector.connect( host = self.db_config['host'], user = self.db_config['username'], passwd = "", db = self.db_config['database'], autocommit=True )
        self._db_cur = self._db_connection.cursor(dictionary=True)
        return self._db_cur

    def __exit__(self, *a):
        if( self._db_connection  ):
            self._db_connection.close()
        else:
            print("no connection to close")
    def __del__(self):
        if( self._db_connection  ):
            self._db_connection.close()
        else:
            print("no connection to close")