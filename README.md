# Diss Spam Call

## 更新记录

@19.04.09 更新：精简代码，仅保留diss骚扰电话的核心功能，增加验证码识别功能（识别度较低）。
@18.7.12 更新：当前版本已失效，百度离线包已增加验证码功能。尚无精力继续鼓捣。

## 功能

借助百度离线宝（莆田系的医院网站使用的那种回拨电话功能），将骚扰你的电话号码随机提交给这些网站商户，使其被这些广告商户骚扰，来达到腹黑目的。

## 使用

MacOs 使用 homebrew 安装 pipenv tesserct：

`brew install pipenv tesseract`

*注：pipenv 是一个非常好使的python包和虚拟环境管理的工具（推荐），tesserct为orc图片识别库。其他系统安装方法自行 Google。

初始化 pipenv，安装依赖包:

`pipenv install`

激活虚拟环境:

`pipenv shell`

启动服务：

`python diss_spam_call.py`

## 说明

当前版本仅提供了使用离线包diss骚扰电话的思路，没有之前微信公众号那一堆业务代码了。目前验证码识别准确度还很低，有精力的可以自行折腾tesserct的学习训练。

## 依赖库

1. requests
2. pillow
3. pytesseract