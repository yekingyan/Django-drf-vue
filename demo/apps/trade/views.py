from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import (
    OrderDetailSerializer, ShopCartSerializer,
    ShopCartDetailSerializer, OrderInfoSerializer,
)

from utils.permissions import IsOwnerOrReadOnly
# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车
    list:
        购物车详情列表
    create:
        加入购物车
    destroy:
        删除购物车商品
    """
    serializer_class = ShopCartSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        serializer_action = {
            'list': ShopCartDetailSerializer,
            'retrieve': ShopCartDetailSerializer,
            'create': ShopCartSerializer,
            'update': ShopCartSerializer,
        }
        return serializer_action.get(self.action, ShopCartDetailSerializer)

    def perform_create(self, serializer):
        """
        加入购物车，商品库存相应减少
        """
        shop_cat = serializer.save()
        goods = shop_cat.goods
        goods.goods_num -= shop_cat.nums
        goods.save()

    def perform_destroy(self, instance):
        """
        移出购物车，商品库存相应增加
        """
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        """
        修改购物车数量
        """
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_num = existed_record.nums
        saved_record = serializer.save()
        nums = existed_num - saved_record.nums
        goods = saved_record.goods
        goods.nums += nums
        goods.save()


class OrderViewSet(viewsets.ModelViewSet):
    """
    list:
        个人订单列表
    destroy:
        删除订单
    create:
        新增订单
    retrieve:
        查看订单详情
    """
    serializer_class = OrderInfoSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        serializer_action = {
            'retrieve': OrderDetailSerializer,
            'list': OrderInfoSerializer,
        }
        return serializer_action.get(self.action, OrderInfoSerializer)

    def perform_create(self, serializer):
        """
        执行生成操作
        """
        # 保存订单到OrderInfo
        order = serializer.save()

        # 保存购物车中的商品到OrderGoods
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods_nums = shop_cart.nums
            order_goods.goods = shop_cart.goods  # goods外键
            order_goods.order = order  # order外键
            order_goods.save()

            # 清空购物车
            shop_cart.delete()
        return order
