from flask import Blueprint
from app.controller import reminder_controller  # 导入 reminder_controller 模块

reminders_blueprint = Blueprint('reminders', __name__)

# 将视图函数与蓝图关联
reminders_blueprint.route('/reminder_list',
                          methods=['GET'])(reminder_controller.reminder_list)
reminders_blueprint.route('/create_reminder/<int:event_id>',
                          methods=['GET', 'POST'])(reminder_controller.create_reminder)
reminders_blueprint.route('/delete_reminder/<int:reminder_id>',
                          methods=['POST'])(reminder_controller.delete_reminder)
