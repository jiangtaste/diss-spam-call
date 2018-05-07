""" 程序运行入口 """
import os
from app import create_app

app = create_app(os.getenv('ENV'))

if __name__ == '__main__':
    app.run()