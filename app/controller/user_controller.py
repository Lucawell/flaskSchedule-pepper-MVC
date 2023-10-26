# encoding:utf-8
from app.model.User import User
from app import app, db
from flask import request, render_template, url_for, redirect

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