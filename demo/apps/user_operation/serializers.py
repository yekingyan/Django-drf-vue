from django.contrib.auth import get_user

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
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
