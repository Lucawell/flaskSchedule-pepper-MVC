from flask_restful import Resource, reqparse
from app.model.Event import Event
from datetime import timedelta, datetime

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
