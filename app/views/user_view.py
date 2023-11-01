# user_view.py
from flask import Blueprint, flash, redirect, url_for, request
from flask_login import current_user
from app.controller import user_controller

user_blueprint = Blueprint('user', __name__)

user_blueprint.route('/register', methods=['GET', 'POST'])(user_controller.register)
user_blueprint.route('/login', methods=['GET', 'POST'])(user_controller.login)
user_blueprint.route('/logout', methods=['GET'])(user_controller.logout)
