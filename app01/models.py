from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=32,verbose_name="姓名")
    pwd=models.CharField(max_length=63,verbose_name="密码")

    def __str__(self):
        return self.name

class ClassList(models.Model):
    captions=models.CharField(max_length=32,verbose_name="班级名称")

    def __str__(self):
        return self.captions