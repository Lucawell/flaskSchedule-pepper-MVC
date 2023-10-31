# 目录介绍

```
│  README.md
│  runserver.py //项目启动文件
│  secrete.py  //密钥生成程序
│  requirements.txt //项目依赖
│  schedule.sql //数据库文件
├─app
│  │  setting.py //配置文件,数据库连接(需要在环境变量中加入此路径)
│  │  forms.py //验证表单程序
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
│  ├─static //静态资源，css，js等
│  ├─templates //MCVC中的视图(V)
│  │      events.html
│  │      index.html //主页
│  │      reminders.html
│  │      users.html
│  │      create_event.html //创建事件
│  │      edit_event.html //编辑事件
│  │      event_list.html //查看事件
│  │      login.html //登录
│  │      register.html //注册

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
from flask_login import LoginManager, current_user, login_required  
  
# 创建项目对象  
app = Flask(__name__)  
app.config.from_object('app.config') # 模块下的config文件名，不用加py后缀  
app.config.from_envvar('FLASKR_CONFIGS') # 环境变量，指向配置文件config的路径  
# 创建数据库对象  
db = SQLAlchemy(app)  
# 登录配置  
login_manager = LoginManager(app)  
login_manager.init_app(app)  
login_manager.login_view = 'login' # 设置登录视图的名称（在这个示例中是 'login'）  
  
# app 導入後才能import  
from app.model import User, Event, Reminder  
# 只有在app对象之后声明，用于导入view模块  
from app.controller import user_controller, event_controller, message_controller, reminder_controller
```

## runserver.py

```python
from app import app  
from app.model.User import User  
from app.model.Event import Event  
from app.model.Reminder import Reminder  
from flask import render_template  
  
@app.route('/')  
def index():  
users = User.query.all()  
events = Event.query.all()  
reminders = Reminder.query.all()  
  
return render_template('index.html', users=users, events=events, reminders=reminders)  
  
if __name__ == '__main__':  
app.run(host='0.0.0.0', port=5000, debug=True)
```
# 数据库E-R图

![image.png](https://img-1313049298.cos.ap-shanghai.myqcloud.com/note-img/202310281756483.png)


# 运行项目

```cmd
python runserver.py
```

# 参考链接

https://tutorial.helloflask.com/
https://flask-login-cn.readthedocs.io/zh/latest/
https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
https://learnku.com/docs/python-learning
https://flask-wtf.readthedocs.io/en/1.2.x/