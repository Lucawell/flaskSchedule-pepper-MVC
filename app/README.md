# 目录介绍

```
│  runserver.py //项目启动文件
│  secrete.py  //密钥生成程序
│  requirements.txt //项目依赖
│  schedule.sql //数据库文件
├─app
│  │  README.md
│  │  setting.py //配置文件,数据库连接(需要在环境变量中加入此路径)
│  │  __init__.py //模块初始化文件，Flask 程序对象的创建须在 __init__.py 文件里完成
│  │
│  ├─controller //MVC中的控制器(C)
│  │  │  event_controller.py //事件控制器
│  │  │  message_controller.py //消息控制器
│  │  │  reminder_controller.py //提醒控制器
│  │  │  user_controller.py //用户控制器
│  │  
│  ├─model //MVC中的模型,数据库中的表(M)
│  │  │  Event.py //事件表
│  │  │  Reminder.py //提醒表
│  │  │  User.py //用户表
│  │
│  ├─static //静态资源
│  ├─templates //MCVC中的视图(V)
│  │      events.html
│  │      index.html
│  │      reminders.html
│  │      users.html
```

# 项目依赖

**python 3.8**

# 配置文件

## setting.py

```python
# encoding:utf-8  
#调试模式是否开启  
DEBUG = True  
# 是否追踪对象的修改。  
SQLALCHEMY_TRACK_MODIFICATIONS = True  
# 查询时显示原始SQL语句  
SQLALCHEMY_ECHO = True  
#session必须要设置key  
SECRET_KEY='c798ee1f5fd894f6e0ba9fc0d16b8b22'  
  
#mysql数据库连接信息  
DATABASE = 'schedule'  
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost/" + DATABASE
```

## \_\_init\_\_.py

```python
# encoding:utf-8  
from flask import Flask  
from flask_sqlalchemy import SQLAlchemy  
  
# 创建项目对象  
app = Flask(__name__)  
  
app.config.from_object('app.setting') # 模块下的setting文件名，不用加py后缀  
app.config.from_envvar('FLASKR_SETTINGS') # 环境变量，指向配置文件setting的路径  
  
# 创建数据库对象  
db = SQLAlchemy(app)  
  
# app导入才能import,模型初始化  
from app.model import User, Event, Reminder  
  
# 只有在app对象之后声明，用于导入view模块,控制器初始化  
from app.controller import user_controller, event_controller, message_controller,reminder_controller
```

# 数据库E-R图

![image.png](https://img-1313049298.cos.ap-shanghai.myqcloud.com/note-img/202310262032300.png)

# 运行项目

```cmd
python runserver.py
```
