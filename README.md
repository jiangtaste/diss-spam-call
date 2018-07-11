# Diss Call

@7.12 更新：当前版本已失效，百度离线包已增加验证码功能。尚无精力继续鼓捣。

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