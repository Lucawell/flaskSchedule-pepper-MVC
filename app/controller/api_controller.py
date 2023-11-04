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
from flask_restful import Resource, fields, marshal_with
from app.model.Event import Event

event_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'title': fields.String,
    'start_time': fields.DateTime,
    'end_time': fields.DateTime,
    'location': fields.String,
    'description': fields.String,
}

class EventResource(Resource):
    @marshal_with(event_fields)
    def get(self, user_id):
        # 根据用户ID查询日程信息
        events = Event.query.filter_by(user_id=user_id).all()
        return events


