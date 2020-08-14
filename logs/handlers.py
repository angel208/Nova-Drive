import logging
from logging.handlers import RotatingFileHandler
import sys


# define formaters
default_formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

# define file handler and set formatter
test_handler = RotatingFileHandler( 'logs/test.log' , mode='a', maxBytes=10000, backupCount=5, encoding=None, delay=0)
test_handler.setFormatter(default_formatter)

error_handler = RotatingFileHandler( 'logs/error.log' , mode='a', maxBytes=10000, backupCount=5, encoding=None, delay=0)
error_handler.setFormatter(default_formatter)

default_handler = RotatingFileHandler( 'logs/nova.log' , mode='a', maxBytes=10000, backupCount=5, encoding=None, delay=0)
default_handler.setFormatter(default_formatter)

rest_handler = RotatingFileHandler( 'logs/rest.log' , mode='a', maxBytes=10000, backupCount=5, encoding=None, delay=0)
rest_handler.setFormatter(default_formatter)

login_handler = RotatingFileHandler( 'logs/login.log' , mode='a', maxBytes=10000, backupCount=5, encoding=None, delay=0)
login_handler.setFormatter(default_formatter)

#console handlers
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(default_formatter)



#set levels
test_handler.setLevel(logging.DEBUG)

error_handler.setLevel(logging.ERROR)
default_handler.setLevel(logging.DEBUG)
rest_handler.setLevel(logging.INFO)
login_handler.setLevel(logging.INFO)

stdout_handler.setLevel(logging.DEBUG)

