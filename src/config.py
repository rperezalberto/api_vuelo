from distutils.debug import DEBUG


class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'mysql'
    MYSQL_DB = 'db_vuelos'

config = {
    'development': DevelopmentConfig
}