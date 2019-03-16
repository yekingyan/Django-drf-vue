import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    """

    """
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('id', 'goods')


class UserFavSerializer(serializers.ModelSerializer):
    # 隐藏字段，默认用户选取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        fields = ('user', 'goods', 'id')
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已经收藏'
            )
        ]


class LeavingMessageSerializer(serializers.ModelSerializer):
    """
    用户留言serializer
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')  # 只返回不提交

    class Meta:
        model = UserLeavingMessage
        fields = ('id', 'user', 'message_type', 'subject', 'message', 'file', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')  # 只返回不提交

    mobile = serializers.SerializerMethodField('get_validate_mobile')  # 用mobile 字段 映射 signer_mobile

    def get_validate_mobile(self, obj):
        mobile = obj.signer_mobile
        # 验证手机号码是合法
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码非法')
        return mobile

    class Meta:
        model = UserAddress
        fields = '__all__'
