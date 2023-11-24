# encoding:utf-8
from flask import Blueprint
from app.controller import reminder_controller

reminder_blueprint = Blueprint('reminder', __name__)

reminder_blueprint.route('/send_email', methods=['GET', 'POST'])(reminder_controller.send_reminder_email)
