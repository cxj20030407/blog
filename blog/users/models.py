from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    # 电话号码字段
    mobile = models.CharField(max_length=20, unique=True, blank=True)

    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    # 个人简介
    user_desc = models.TextField(max_length=500, blank=True)

    # 修改认证的字段
    USERNAME_FIELD = 'mobile'

    # 创建超级管理员的需要必须输入的字段
    REQUIRED_FIELDS = ['username', 'email']

    # 修改认证的字段为手机号
    USERNAME_FIELD = 'mobile'
    # 内部类
    class Meta:
        db_table = 'tb_users'              # 修改默认的表名
        verbose_name = '用户信息'         # Admin后台显示
        verbose_name_plural = verbose_name    # Admin后台显示

    def __str__(self):
        return self.mobile



# 测试版本
class Admin(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username