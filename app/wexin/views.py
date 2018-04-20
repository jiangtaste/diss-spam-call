""" 微信视图模块 """
from . import wx


@wx.route('/wx')
def wx():
    """ Wexin """
    return "<h1>Hello World!</h1>"
