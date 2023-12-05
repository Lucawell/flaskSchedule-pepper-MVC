from flask import render_template, request
from flask_restful import Resource, reqparse
from aliyunsdkcore.client import AcsClient
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest
import json
from flask_uploads import UploadSet, IMAGES
from datetime import datetime
from werkzeug.utils import secure_filename

from app.config import ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET, API_TOKEN

# 令牌配置
api_token = API_TOKEN  # 用于身份验证的API令牌


# 事件资源
class EventResource(Resource):
    """
    处理用户事件资源的restful API。
    """
    def get(self, user_id):
        """处理GET请求，获取用户的事件信息。
            Args:
                user_id (int): 用户ID。
            Returns:
                dict: 包含用户今天和已过期事件的字典。
        """
        # 检查请求头中是否包含有效的令牌
        token = request.headers.get("Authorization")
        if token != api_token:
            return {"error": "Unauthorized"}, 401
        # 查询当前用户的所有事件
        from app.controller.event_controller import get_user_events
        today_events, expired_events = get_user_events(user_id)
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


# 接收信息
class MessageStore:
    messages = []


class MessageResource(Resource):
    def post(self):
        """处理POST请求，接收消息。

        Returns:
            dict: 包含接收消息的字典。
        """
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
        """处理POST请求，发送邮件。

        Returns:
            dict: 包含邮件发送状态的字典。
        """
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
        from app.controller.reminder_controller import send_email
        send_email(title, html, recipients)

        return {'message': '邮件发送成功'}, 200


# 阿里云短信配置
access_key_id = ALIYUN_ACCESS_KEY_ID
access_key_secret = ALIYUN_ACCESS_KEY_SECRET
region_id = 'cn-hangzhou'  # 阿里云短信服务所在的区域
# 创建阿里云短信服务客户端
acs_client = AcsClient(access_key_id, access_key_secret, region_id)


# 发送短信
class SMSResource(Resource):
    def post(self):
        """处理POST请求，发送短信。

       Returns:
           dict: 包含短信发送状态的字典。
       """
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
        """使用阿里云短信服务发送短信。

        Args:
            phone_number (str): 接收短信的手机号。
            message (str): 要发送的短信内容。

        Returns:
            dict: 包含短信发送结果的字典。
        """
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


# 上传文件
photos = UploadSet("photos", IMAGES)
class FileUploadResource(Resource):
    def post(self):
        """处理POST请求，上传文件。

       Returns:
           dict: 包含文件上传状态和文件URL的字典。
       """
        try:
            # 检查请求中是否包含“照片”文件
            if "photo" not in request.files:
                return {"error": "No file part"}, 400
            photo = request.files["photo"]
            # 检查是否提供了文件名
            if photo.filename == "":
                return {"error": "No selected file"}, 400
            # 重命名文件-时间戳
            file_extension = secure_filename(photo.filename).rsplit('.', 1)[1].lower()
            filename = f"{int(datetime.timestamp(datetime.now()))}.{file_extension}"
            # 保存文件
            photos.save(photo, name=filename)
            # 获取上传文件的URL
            file_url = photos.url(filename)

            return {"status": "success", "file_url": file_url}, 201

        except Exception as e:
            return {"error": str(e)}, 500
