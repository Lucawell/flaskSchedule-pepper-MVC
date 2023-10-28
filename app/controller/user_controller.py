# encoding:utf-8
from app.model.User import User
from app import app, db
from flask import request, render_template, url_for, redirect, flash
from app.forms import RegisterForm, LoginForm

@app.route("/users")
def user_list():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    new_user = User(name=name, email=email, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('user_list'))


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('user_list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('user_list'))

    return render_template('users.html', user=user)


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('user_list'))


@app.route('/register', methods=['GET', 'POST'])
def register():
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
            return redirect(url_for('register'))

        # 创建新用户
        new_user = User(name=name, email=email, phone=phone, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # form.email.data = "输入您邮箱"  # 设置初始值
    if form.validate_on_submit():
        email = form.email.data  # 修改为使用邮箱作为登录凭据
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # 用户验证成功，将用户标记为已登录
            # 可以使用 Flask-Login 或自己的会话管理逻辑来处理登录状态
            flash('登录成功', 'success')
            return redirect(url_for('user_list'))  # 跳转到用户仪表板或其他受保护的页面
        else:
            flash('登录失败，请检查邮箱或密码', 'error')

    return render_template('login.html', form=form)
