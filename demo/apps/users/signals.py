from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    让密码可以密文保存
    :param sender:
    :param instance: model的实例对象
    :param created: 创建行为
    """
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
        # 用jwt就不用token了
        # Token.objects.create(user=instance)
