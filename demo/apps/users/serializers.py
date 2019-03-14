import re
from datetime import (
    datetime,
    timedelta
)

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册检验
    """
    # code不会保存到数据库中
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='验证码',
                                 error_messages={
                                     'blank': '不能为空字符串',
                                     'min_length': '太短了',
                                 },
                                 help_text="验证码")
    username = serializers.CharField(required=True, allow_blank=False, help_text='用户名', label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')]
                                     )
    password = serializers.CharField(label='密码', write_only=True, help_text='密码')

    class Meta:
        model = User
        fields = ('username', 'code', 'password')

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        five_mintes_ago = datetime.now() - timedelta(minutes=5)

        if verify_records:
            last_code = verify_records[0]
            if last_code.code != code:
                raise serializers.ValidationError('验证码错误')
            elif five_mintes_ago > last_code.add_time:
                raise serializers.ValidationError('验证码过期')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        """
        修改参数以符合ModelSerializer要求。活用ModelSerializer，避免报错
        """
        # 补充参数，前端可能没有的参数，而数据库必填的字段
        attrs['mobile'] = attrs['username']

        # 删除参数，验证需要的字段，而数据库没有的字段
        del attrs['code']

        return attrs

    # def create(self, validated_data):
    #     """
    #     让密码可以密文保存
    #     """
    #     user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
