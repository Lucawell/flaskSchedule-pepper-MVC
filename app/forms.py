# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, DateTimeField, SubmitField


class RegisterForm(FlaskForm):
    name = StringField('用户名', [validators.DataRequired("用户名不能为空")])
    email = StringField('邮箱', [validators.DataRequired("邮箱不能为空"), validators.Email("无效的邮箱地址")])
    phone = StringField('电话')
    password = PasswordField('密码', [
        validators.DataRequired("密码不能为空"),
        validators.Length(min=8, message="密码长度至少 8 个字符")
    ])
    confirm_password = PasswordField('确认密码', [
        validators.DataRequired("请再次输入密码"),
        validators.EqualTo('password', message='两次密码不匹配')
    ])


class LoginForm(FlaskForm):
    email = StringField('邮箱', [validators.DataRequired("邮箱不能为空"), validators.Email("无效的邮箱地址")])
    password = PasswordField('密码', [validators.DataRequired("密码不能为空")])


class EventForm(FlaskForm):
    title = StringField('标题', validators=[validators.DataRequired(), validators.Length(max=255)])
    start_time = DateTimeField('开始时间', format='%Y-%m-%d %H:%M', validators=[validators.DataRequired()])
    end_time = DateTimeField('结束时间', format='%Y-%m-%d %H:%M', validators=[validators.DataRequired()])
    location = StringField('地点', validators=[validators.Length(max=255)])
    description = StringField('描述', validators=[validators.Length(max=255)])
    submit = SubmitField('Submit')  # 添加这一行来定义 submit 字段
