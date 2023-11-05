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
from flask_restful import Resource
from app.model.Event import Event
from datetime import timedelta, datetime


def generate_repeat_event(event, current_date):
    new_event = Event(
        user_id=event.user_id,
        title=event.title,
        start_date=current_date,
        end_date=current_date,
        event_time=event.event_time,
        location=event.location,
        description=event.description,
        repeat=event.repeat,
        reminder_type=event.reminder_type,
        reminder_time=event.reminder_time
    )
    new_event.id = event.id  # 设置新事件的ID为原事件的ID
    return new_event


class EventResource(Resource):
    def get(self, user_id):
        # 查询当前用户的所有事件
        events = Event.query.filter_by(user_id=user_id).all()
        today = datetime.now().date()  # 获取当前日期
        today_events = []

        for event in events:
            if event.repeat == "none" and event.start_date <= today <= event.end_date:
                today_events.append(event)
            else:
                start_date = event.start_date
                end_date = event.end_date

                if event.repeat == "daily":
                    current_date = start_date
                    while current_date <= end_date:
                        if current_date >= today:
                            new_event = generate_repeat_event(event, current_date)
                            today_events.append(new_event)
                            break
                        current_date += timedelta(days=1)
                elif event.repeat == "weekly":
                    current_date = start_date
                    while current_date <= end_date:
                        if current_date >= today:
                            last_week_event = generate_repeat_event(event, current_date)
                            today_events.append(last_week_event)
                            break
                        current_date += timedelta(weeks=1)

        # 将事件对象转换为 JSON 格式返回给客户端
        event_data = [
            {"id": event.id,
             "title": event.title,
             "event_time": str(event.event_time),
             "start_date": str(event.start_date),
             "end_date": str(event.end_date),
             "location": event.location,
             "description": event.description,
             } for event in today_events
        ]
        return {"events": event_data}
