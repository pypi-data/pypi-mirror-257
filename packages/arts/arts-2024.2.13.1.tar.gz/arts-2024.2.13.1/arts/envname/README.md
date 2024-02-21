# 项目描述

为运行环境设置名称。

有时候，对于某些功能，我们也许希望在不同的环境上采用不同的方案。以访问数据库为例：当程序在外网运行时，须通过数据库公网ip访问；而当程序在内网运行时，为了提高性能，我们可以通过数据库内网ip访问。

# 作者信息

昵称：江南雨上

[主页](https://lcctoor.github.io/arts/) \| [微信](https://lcctoor.github.io/arts/arts/ip_static/WeChatQRC.jpg) \| [Github](https://github.com/lcctoor) \| [PyPi](https://pypi.org/user/lcctoor) \| [邮箱](mailto:lcctoor@outlook.com) \| [捐赠](https://lcctoor.github.io/arts/arts/ip_static/DonationQRC-0rmb.jpg)

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/arts/issues)、[微信](https://lcctoor.github.io/arts/arts/ip_static/WeChatQRC.jpg) 与我联系。

# 安装

```
pip install envname
```

# 教程 ([查看美化版](https://lcctoor.github.io/arts/arts/envname) 👈)

## 创建环境名称

（cmd）：

```
envname set aliyun_hongkong_1
```

注：

1、名称不能包含空格和引号。

2、名称可以包含中文。

3、名称不限长度。

## 查看环境名称

（cmd）：

```
envname read
```

## 导入环境名称

```python
from envname import EnvName
```

## 示例

```python
import pymysql
from envname import EnvName

if EnvName == 'aliyun_hongkong_1':
    host = '192.168.0.127'
else:
    host = '112.47.203.101'

conn = pymysql.connect(host=host, port=3306, user='root', password='123456789')
```
