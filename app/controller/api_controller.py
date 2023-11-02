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
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse, fields, marshal_with
from app.model.Event import Event
from app import db

# 定义用于格式化事件数据的字段
event_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'title': fields.String,
    'start_time': fields.DateTime(dt_format='iso8601'),
    'end_time': fields.DateTime(dt_format='iso8601'),
    'location': fields.String,
    'description': fields.String,
}


class EventListResource(Resource):
    @jwt_required  # 使用 JWT Token 进行身份验证

    @marshal_with(event_fields)
    def get(self):
        current_user_id = get_jwt_identity()  # 获取当前用户的 ID（从 JWT Token 中提取）
        # 查询与当前用户相关的事件
        events = Event.query.filter_by(user_id=current_user_id).all()
        return events



