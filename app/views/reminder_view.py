# encoding:utf-8
from flask import Blueprint
from app.controller import reminder_controller

reminder_blueprint = Blueprint('reminder', __name__)

reminder_blueprint.route('/send_email', methods=['GET', 'POST'])(reminder_controller.send_reminder_email)
reminder_blueprint.route('/email_history')(reminder_controller.show_email_history)
reminder_blueprint.route('/delete_email_history/<int:email_history_id>', methods=['POST'])(reminder_controller.delete_email_history)
