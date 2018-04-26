""" 程序运行入口 """
from flask import Flask
from raven.contrib.flask import Sentry

centry = Sentry()


def create_app():
    """ 工厂模式 """
    app = Flask(__name__)

    centry.init_app(app)

    from .wexin import wx as wx_blueprint
    app.register_blueprint(wx_blueprint)

    return app
