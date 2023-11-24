# encoding:utf-8
from flask import Blueprint, render_template, redirect, url_for

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/')
def home():
    # return render_template('index.html')
    return redirect(url_for('event.show_event'))  # 重定向到事件列表页面或其他适当的页面

