""" 程序运行入口 """
from flask import Flask
# flask扩展
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

# 配置文件
from config import Config

db = SQLAlchemy()
redis_store = FlaskRedis()


def create_app(env):
    """ 工厂模式 """
    app = Flask(__name__)
    app.config.from_object(Config[env])

    db.init_app(app)
    redis_store.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app