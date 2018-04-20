""" 程序运行入口 """
from flask import Flask


def create_app():
    """ 工厂模式 """
    app = Flask(__name__)

    from .wexin import wx as wx_blueprint
    app.register_blueprint(wx_blueprint)

    return app
