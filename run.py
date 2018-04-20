""" 程序运行入口 """
from flask import Flask

app = Flask(__name__)


@app.route('/wx')
def wx():
    """ Demo """
    return "<h1>Hello World!</h1>"


if __name__ == '__main__':
    app.run()