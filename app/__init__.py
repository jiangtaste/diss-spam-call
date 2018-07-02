""" 程序运行入口 """
import firebase_admin
from flask import Flask
from raven.contrib.flask import Sentry
from flask_redis import FlaskRedis

from firebase_admin import credentials
from firebase_admin import firestore

from config import Config

sentry = Sentry()
redis_store = FlaskRedis()

# 初始化firebase
cred = credentials.Certificate("app/firebase_key.json")
firebase_admin.initialize_app(cred)

# firestore
fire_store = firestore.client()


def create_app(env):
    """ 工厂模式 """
    app = Flask(__name__)
    app.config.from_object(Config[env])

    sentry.init_app(app)
    redis_store.init_app(app)

    from .weixin import wx as wx_blueprint
    app.register_blueprint(wx_blueprint)

    return app