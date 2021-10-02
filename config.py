import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_123')


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True