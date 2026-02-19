
class Config(object):
    SECRET_KEY='root'
    SESSION_COOKIE_SECURE=False

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@127.0.0.1/idgs802'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
