import mysql.connector
import configparser
import os

def get_connection():
    config = configparser.ConfigParser()

    # Build absolute path to config/config.ini safely
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
    config.read(config_path)

    if 'mysql' not in config:
        raise Exception("'mysql' section not found in config.ini")

    db = config['mysql']
    return mysql.connector.connect(
        host=db['host'],
        user=db['user'],
        password=db['password'],
        database=db['database']
    )

