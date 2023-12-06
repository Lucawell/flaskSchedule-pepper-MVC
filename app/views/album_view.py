# encoding:utf-8
from flask import Blueprint, render_template, url_for, current_app
import os

album_blueprint = Blueprint('album', __name__)


@album_blueprint.route('/album_list')
def album_list():
    image_paths = get_image_paths()
    return render_template('album.html', image_paths=image_paths)


def get_image_paths():
    image_paths = []
    for root, dirs, files in os.walk(r'app\static\uploads'):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                path = os.path.relpath(os.path.join(root, file), os.path.join('app', 'static'))
                image_paths.append(path.replace(os.path.sep, '/'))
    print(image_paths)
    return image_paths
