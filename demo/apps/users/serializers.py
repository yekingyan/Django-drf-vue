import re
from datetime import (
    datetime,
    timedelta
)

from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    不用serializers.ModelSerializer，是因为code是必填字段
    而刚获取时没有code，会出错
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count() > 0:
            raise serializers.ValidationError('用户已存在')

        # 验证手机号码是合法
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码非法')

        # 验证发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, code=mobile).count():
            raise serializers.ValidationError('距离上次发送未超过60秒')

        return mobile
