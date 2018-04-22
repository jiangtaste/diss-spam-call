""" 微信蓝本 """
from flask import Blueprint

wx = Blueprint('wx', __name__)

from . import views, templates