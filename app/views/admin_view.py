from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import AdminIndexView


# 自定义页面
# class HelloView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('admin_dashboard.html')

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class UserAdminView(ModelView):
    column_searchable_list = ('name', 'email')
    column_sortable_list = ('name', 'is_admin')
    # 隐藏列
    column_exclude_list = ('password_hash',)
    # 禁止编辑列
    form_excluded_columns = ('password_hash',)
    # 可编辑列
    form_edit_rules = ('name', 'email', 'phone', 'is_admin')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class EventAdminView(ModelView):
    column_searchable_list = ('user_id',)
    column_list = ('user.name', 'user_id', 'title', 'start_date', 'event_time', 'end_date',
                   'location', 'description', 'repeat', 'reminder_type', 'reminder_time')
    column_formatters = {
        'user.name': lambda view, context, model, name: model.user.name  # 假设user有一个name字段
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class EmailHistoryAdminView(ModelView):
    column_searchable_list = ('user_id',)
    column_list = ('user.name', 'user_id', 'title', 'content', 'recipients', 'sent_at')

    column_formatters = {
        'user.name': lambda view, context, model, name: model.user.name  # 假设user有一个name字段
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
