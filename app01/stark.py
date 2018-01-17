from stark.service import start
from django.utils.safestring import mark_safe
from app01 import models

class UserConfig(start.ModelConfig):


    list_display = ["id", "name", "pwd"]


start.site.register(models.User,UserConfig)
start.site.register(models.ClassList)