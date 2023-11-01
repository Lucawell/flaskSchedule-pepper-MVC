# encoding:utf-8
from flask import Blueprint, render_template

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/')
def home():
    return render_template('index.html')
