# encoding:utf-8
from flask import flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import RegisterForm, LoginForm
from app.model.User import User
from app import db, login_manager


def register():
    """
    注册新用户。

    该函数处理新用户的注册过程。它验证用户提交的表单数据，
    检查用户是否已存在，在数据库中创建新用户，并将用户重定向到登录页面
    注册成功后。

    Returns:
        如果表单数据有效并且用户注册成功，则将用户重定向到登录页面。
        否则，它会呈现带有注册表单的 register.html 模板。

    """
    form = RegisterForm()
    if form.validate_on_submit():
        # 获取用户提交的数据
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        password = form.password.data

        # 检查用户是否已存在
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('该邮箱地址已被注册', 'error')
            return redirect(url_for('user.register'))

        # 创建新用户
        new_user = User(name=name, email=email, phone=phone, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功，请登录', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)

def login():
    """
    用户登录函数

    如果用户已登录，则重定向到受保护的页面。
    如果用户提交了有效的登录表单，则验证用户凭据并将用户标记为已登录。
    如果用户验证失败，则显示错误消息。

    return: 渲染登录页面或重定向到受保护的页面
    """
    if current_user.is_authenticated:
        # 如果用户已登录，重定向到受保护的页面
        return redirect(url_for('event.show_event'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data  # 修改为使用邮箱作为登录凭据
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # 用户验证成功，将用户标记为已登录
            # 可以使用 Flask-Login 或自己的会话管理逻辑来处理登录状态
            login_user(user,remember=form.remember)
            flash('登录成功', 'success')
            return redirect(url_for('event.show_event'))  # 跳转到用户仪表板或其他受保护的页面
        else:
            flash('登录失败，请检查邮箱或密码', 'error')

    return render_template('login.html', form=form)

@login_required
def logout():
    logout_user()  # 使用 Flask-Login 注销用户
    flash('成功注销', 'success')
    return redirect(url_for('user.login'))

@login_manager.user_loader
def load_user(user_id):
    # 使用用户 ID 查询用户对象
    return User.query.get(int(user_id))