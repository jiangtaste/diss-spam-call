# Diss Call

v0.9.0 开始将微信公众号业务和反骚扰服务分开，这里仅含Diss Call业务

## 工具链

pipenv, python3.6.5, Flask 1.0+, Redis

## 使用

MacOs使用homebrew安装pipenv，其他系统自行Google:

`brew install pipenv`

初始化pipenv，安装依赖包:

`pipenv install`

配置环境变量.env：

``` shell
FLASK_APP=run.py
FLASK_ENV=development
ENV=development
REDIS_URL=redis://:passwd@localhost:6379/0
SECRET_KEY=yourSecretKey
```

启动flask dev服务:

`pipenv run flask run`

访问localhost:5000?num=phoneNumber开始你的腹黑之旅