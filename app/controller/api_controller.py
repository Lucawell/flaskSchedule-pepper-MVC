# # encoding:utf-8
# from app.model.User import User
# from app import app
# from flask import request, jsonify

# ----------------------------------以下是测试部分，不要在生产环境调用-----------------------------------
# 发送消息
# @app.route("/getdata")
# def getdata():
#     # 查询所有用户记录
#     users = User.query.all()
#     # 创建一个 JSON 对象
#     json_data = []
#     for user in users:
#         # 将用户记录添加到 JSON 对象
#         json_data.append({
#             "id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "phone": user.phone
#         })
#     # 使用 jsonify() 函数来序列化 JSON 对象
#     json_response = jsonify(json_data)
#
#     # 使用 return 语句返回 JSON 对象
#     return json_response
#
# # 接收消息
# @app.route('/receive_message', methods=['POST', 'GET'])
# def receive_message():
#     if request.method == 'POST':
#         data = request.form.get('message')
#         print("Received message:", data)
#         if data:
#             return data  # 返回消息文本
#         else:
#             return "No message received."
#     else:
#         return "GET request received."
# ----------------------------------以下是用户环境-----------------------------------
from flask import Blueprint, request, jsonify
from flask_login import login_user
from app.forms import LoginForm
from app.model.User import User

api_login_blueprint = Blueprint('api_login', __name__)

@api_login_blueprint.route('/api/login', methods=['POST'])
def api_login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)  # 使用 Flask-Login 登录用户

            # 如果登录成功，可以返回成功的响应，也可以返回用户信息
            response = {
                "message": "登录成功",
                "user_id": user.id,
                "user_name": user.name,
                # 其他用户信息
            }
            return jsonify(response), 200
        else:
            response = {
                "message": "登录失败，请检查邮箱或密码"
            }
            return jsonify(response), 401  # 401 表示未授权

    response = {
        "message": "请求参数无效"
    }
    return jsonify(response), 400  # 400 表示请求无效

