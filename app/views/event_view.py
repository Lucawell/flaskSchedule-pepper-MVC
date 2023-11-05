# event_view.py
from flask import Blueprint
from app.controller import event_controller  # 导入 event_controller 模块

event_blueprint = Blueprint('event', __name__)

# 将视图函数与蓝图关联
event_blueprint.route('/event_list')(event_controller.show_event)
event_blueprint.route('/create_event', methods=['GET', 'POST'])(event_controller.create_event)
event_blueprint.route('/delete_event/<int:event_id>', methods=['POST'])(event_controller.delete_event)
event_blueprint.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])(event_controller.edit_event)
