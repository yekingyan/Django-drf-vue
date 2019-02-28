from datetime import datetime

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'姓名')
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(choices=(('male', u'男'), ('female', u'女')), default='male', max_length=6)
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    # image = models.ImageField(upload_to='image/%Y/%m', default=u'image/default.png', max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='邮箱')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        # username 继承于 AbstractUser
        return str(self.name)


class VerifyCode(models.Model):
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
