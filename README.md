# 目录介绍

```
│  README.md
│  runserver.py //项目启动文件
│  secrete.py  //密钥生成程序
│  requirements.txt //项目依赖
│  schedule.sql //数据库文件
├─app
│  │  config.py //配置文件,数据库连接(需要在环境变量中加入此路径)
│  │  forms.py //验证表单程序
│  │  __init__.py //模块初始化文件，Flask 程序对象的创建须在 __init__.py 文件里完成
│  │
│  ├─controller //MVC中的控制器(C)
│  │     event_controller.py //事件控制器
│  │     api_controller.py //api控制器
│  │     user_controller.py //用户控制器
│  │  
│  ├─model //MVC中的模型,数据库中的表(M)
│  │     Event.py //事件表
│  │     User.py //用户表
│  │
│  ├─views //MVC中的视图(V)
│  │     admin_view.py
│  │     event_view.py
│  │     index_view.py
│  │     user_view.py
│  │ 
│  ├─static //静态资源，css，js等
│  ├─templates //视图映射的页面
│  │      index.html //主页
│  │      create_event.html //创建事件
│  │      edit_event.html //编辑事件
│  │      event_list.html //查看事件
│  │      login.html //登录
│  │      register.html //注册

```

# 项目依赖

**python-3.8 ;mysql-15.1**

# 配置文件

## config.py

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
# # encoding:utf-8  
from flask import Flask  
from flask_sqlalchemy import SQLAlchemy  
from flask_login import LoginManager  
from flask_migrate import Migrate  
from flask_restful import Api  
from flask_admin import Admin  
  
  
db = SQLAlchemy()  
login_manager = LoginManager()  
migrate = Migrate()  
  
  
def create_app():  
app = Flask(__name__)  
app.config.from_object('app.config')  
app.config.from_envvar('FLASKR_CONFIGS')  
# 初始化数据库  
db.init_app(app)  
# 注册migrate，创建数据库迁移  
migrate.init_app(app, db)  
# 登录管理  
login_manager.init_app(app)  
login_manager.login_view = 'user.login' # 设置登录视图的名称（在这个示例中是 'user.login'）  
  
# api管理  
api = Api(app)  
  
# 导入数据库模型  
from app.model.User import User  
from app.model.Event import Event  
  
# 导入视图  
from app.views.index_view import index_blueprint  
from app.views.user_view import user_blueprint  
from app.views.event_view import event_blueprint  
import app.views.admin_view as views  
  
# 导入控制器  
from app.controller.api_controller import EventResource  
  
# 注册蓝图  
app.register_blueprint(index_blueprint, url_prefix='/')  
app.register_blueprint(user_blueprint, url_prefix='/user')  
app.register_blueprint(event_blueprint, url_prefix='/event')  
  
# 将资源添加到您的 APIapi.add_resource(EventResource, '/api/events/<int:user_id>')  
  
# 管理员  
admin = Admin(app, index_view=views.MyAdminIndexView())  
admin.add_view(views.UserAdminView(User, db.session, url='users', name='users', endpoint='users_admin'))  
admin.add_view(views.admin'))  
  
return app
```

## runserver.py

```python
from app import create_app  
  
if __name__ == '__main__':  
app = create_app()  
app.run(host='0.0.0.0', port=5000, debug=True)
```
# 数据库
## E-R图

![image.png](https://img-1313049298.cos.ap-shanghai.myqcloud.com/note-img/202311051315126.png)


## 数据库迁移

创建迁移存储库：

```bash
flask db init
```

这会将迁移文件夹添加到应用程序中。此时，你可以发现项目目录多了一个 migrations 的文件夹，下边的 versions 目录下的文件就是生成的数据库迁移文件！

然后，运行以下命令生成迁移
```bash
flask db migrate -m "initial migration"
```

做完这两步就完成了第一次的初始迁移操作，我们可以看数据库已经有了我们创建的模型字段！之后，每次在新增和修改完模型数据之后，只需要执行以下两个命令即可
```bash
flask db migrate -m "description of changes"
flask db upgrade
```

这些步骤将允许你使用`flask_migrate`管理数据库模型的变化。请确保按照这些步骤在你的Flask应用中设置并使用`flask_migrate`，以便维护数据库模型的一致性。

#  运行项目

```cmd
python runserver.py
```

## 管理员页面

使用flask-admin插件

http://127.0.0.1:5000/admin/

## 
    
# 参考链接

https://tutorial.helloflask.com/
https://flask-login-cn.readthedocs.io/zh/latest/
https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
https://learnku.com/docs/python-learning
https://flask-wtf.readthedocs.io/en/1.2.x/
https://dormousehole.readthedocs.io/en/latest/
https://www.zlkt.net/post/detail/60
https://pythonhosted.org/Flask-JWT/
https://github.com/apachecn/apachecn-pythonweb-zh/blob/master/docs/flask-framework-cb/08.md