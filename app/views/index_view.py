# encoding:utf-8
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.controller.event_controller import get_user_events

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/')
@login_required
def home():
    user_id = current_user.id  # 假设您有一个 current_user 对象
    today_events, expired_events = get_user_events(user_id)
    return render_template('index.html', events=today_events, expired_events=expired_events)
