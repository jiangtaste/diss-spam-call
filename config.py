""" App config file """
import os


class Config(object):
    """ 配置基类 """

    SECRET_KEY = os.getenv('SECRET_KEY')
    REDIS_URL = os.getenv('REDIS_URL')


class DevConfig(Config):
    """ 开发环境配置 """

    pass


class ProdConfig(Config):
    """ 生产环境配置 """

    pass


Config = {'development': DevConfig, 'production': ProdConfig}
