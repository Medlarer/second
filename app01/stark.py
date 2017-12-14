from stark.service import start
from django.utils.safestring import mark_safe
from app01 import models

class UserConfig(start.ModelConfig):

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return "选择"
        return mark_safe("<input type='checkbox' name='choice' value='%s'>" %(obj.id,))
    def edit(self,obj=None,is_header=False):
        if is_header:
            return "编辑"
        return mark_safe("<a href='edit/%s'>编辑</a>" %(obj.id,))
    list_display = [checkbox, "id", "name", "pwd", edit]


start.site.register(models.User,UserConfig)
start.site.register(models.ClassList)