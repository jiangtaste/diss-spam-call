# Diss Call

@7.12 更新：当前版本已失效，百度离线包已增加验证码功能。尚无精力继续鼓捣。

## 工具链

pipenv, python3.7.2, Flask 1.0+, Redis

## 使用

MacOs 使用 homebrew 安装 pipenv，其他系统自行 Google:

`brew install pipenv`

初始化 pipenv，安装  依赖包:

`pipenv install`

配置环境变量.env：

```shell
FLASK_APP=run.py
FLASK_ENV=development
ENV=development
REDIS_URL=redis://:passwd@localhost:6379/0
SECRET_KEY=yourSecretKey
```

启动 flask dev 服务:

`pipenv run flask run`

访问 localhost:5000?num=phoneNumber 开始你的腹黑之旅
