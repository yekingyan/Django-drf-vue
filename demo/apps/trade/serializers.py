import time
import random

from rest_framework import serializers

from goods.models import Goods
from goods.serializers import GoodsSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = ShoppingCart
        fields = '__all__'


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


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    orderGoods = OrderGoodsSerializer(many=True)
    add_time = serializers.DateTimeField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)

    def _generate_order_sn(self):
        """
        生成订单号
        当前时间 + user_id + 随机数
        """
        time_str = time.strftime('%Y%m%d%H%M%S')
        user_id = self.context['request'].user.id
        random_str = ''.join(random.sample('1234567890', 2))

        order_sn = f'{time_str}{user_id}{random_str}'
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self._generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'
