import configparser

#function that finds a config value from the app_config section of the config.ini file
def  get_app_config( config_key ):

    config = configparser.ConfigParser()
    config.read('config.ini')

    return config['app_config'][config_key]

def  get_app_config( config_key ):

    config = configparser.ConfigParser()
    config.read('config.ini')

    return config['app_config'][config_key]


