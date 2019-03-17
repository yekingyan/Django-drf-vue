from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                        'min_value': '商品数量不能小于1',
                                        'required': '请选择购买的数量',
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            # 更新， 购物车存在纪录，则数量加上新传入的数量参数
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            # 创建， 购物车不存在纪录
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        """
        修改商品数量
        """
        instance.nums = validated_data['nums']
        instance.save()
        return instance
