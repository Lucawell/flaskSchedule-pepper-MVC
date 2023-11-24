from flask import render_template, request
from flask_restful import Resource, reqparse
from app.model.Event import Event
from datetime import timedelta, datetime
from app.controller.reminder_controller import send_email
from aliyunsdkcore.client import AcsClient
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest
import json
from app.config import ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET, API_TOKEN

# 令牌配置
api_token = API_TOKEN


# 事件资源
class EventResource(Resource):
    def get(self, user_id):
        # 检查请求头中是否包含有效的令牌
        token = request.headers.get("Authorization")
        if token != api_token:
            return {"error": "Unauthorized"}, 401
        # 查询当前用户的所有事件
        events = Event.query.filter_by(user_id=user_id).all()
        today = datetime.now().date()  # 获取当前日期
        today_events = []
        expired_events = []
        for event in events:
            # 如果事件过期，将其添加到过期事件列表中
            if event.end_date < today:
                expired_events.append(event)
                continue
            # 如果事件不是重复事件，将其添加到今天事件列表中
            if event.repeat == "none" and today <= event.end_date:
                today_events.append(event)
            # 如果事件是重复事件，动态生成后将其添加到今天事件列表中
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
                    if end_date - today < timedelta(days=7):
                        expired_events.append(event)
                        continue
                    current_date = start_date
                    while current_date <= end_date:
                        if current_date >= today:
                            last_week_event = generate_repeat_event(event, current_date)
                            today_events.append(last_week_event)
                            break
                        current_date += timedelta(weeks=1)
                elif event.repeat == "monthly":
                    if end_date - today < timedelta(days=30):
                        expired_events.append(event)
                        continue
                    current_date = start_date
                    while current_date <= end_date:
                        if current_date >= today:
                            last_month_event = generate_repeat_event(event, current_date)
                            today_events.append(last_month_event)
                            break
                        current_date += timedelta(days=30)

        # 将事件对象转换为 JSON 格式返回给客户端
        event_today = [
            {"id": event.id,
             "title": event.title,
             "event_time": str(event.event_time),
             "start_date": str(event.start_date),
             "end_date": str(event.end_date),
             "location": event.location,
             "description": event.description,
             } for event in today_events
        ]
        expired_events = [
            {"id": event.id,
             "title": event.title,
             "event_time": str(event.event_time),
             "start_date": str(event.start_date),
             "end_date": str(event.end_date),
             "location": event.location,
             "description": event.description,
             } for event in expired_events
        ]
        return {"events": event_today, "expired_events": expired_events}

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


# 接收信息
class MessageStore:
    messages = []


class MessageResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, help='Message to be received', required=True)
        args = parser.parse_args()
        message = args['message']
        MessageStore.messages.append(message)
        print("Received message:", message)
        return {'message': message}


# 发送邮件
class EmailResource(Resource):
    def post(self):
        # 检查请求头中是否包含有效的令牌
        token = request.headers.get("Authorization")
        if token != api_token:
            return {"error": "Unauthorized"}, 401
        title = request.json.get('title')
        content = request.json.get('content')
        recipients = request.json.get('recipients')

        if not title or not content or not recipients:
            return {'message': '缺少必要参数'}, 400

        html = render_template('email_template.html', title=title, content=content)

        send_email(title, html, recipients)

        return {'message': '邮件发送成功'}, 200


# 阿里云短信配置
access_key_id = ALIYUN_ACCESS_KEY_ID
access_key_secret = ALIYUN_ACCESS_KEY_SECRET
region_id = 'cn-hangzhou'  # 阿里云短信服务所在的区域
# 创建阿里云短信服务客户端
acs_client = AcsClient(access_key_id, access_key_secret, region_id)


class SMSResource(Resource):
    def post(self):
        # 检查请求头中是否包含有效的令牌
        token = request.headers.get("Authorization")
        if token != api_token:
            return {"error": "Unauthorized"}, 401

        # 解析请求数据
        data = request.get_json()

        # 从请求数据中获取手机号和短信内容
        phone_number = data.get('phone_number')
        message = data.get('message')
        # 调用阿里云短信服务发送短信
        result = self.send_sms(phone_number, message)

        # 返回发送结果
        return {'status': 'success', 'result': result}

    def send_sms(self, phone_number, message):
        # 构造短信发送请求
        request = SendSmsRequest()
        request.set_TemplateCode('SMS_464060163')  # 替换成你在阿里云短信服务中创建的模板CODE
        request.set_TemplateParam({'message': message})
        request.set_SignName('pepper')  # 替换成你在阿里云短信服务中创建的签名

        # 设置手机号
        request.set_PhoneNumbers(phone_number)

        # 发送短信
        response = acs_client.do_action_with_exception(request)

        return json.loads(response.decode('utf-8'))
