from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import (
    UserFavSerializer, UserFavDetailSerializer,
    LeavingMessageSerializer, AddressSerializer,
)
from utils.permissions import IsOwnerOrReadOnly
from utils.pagination import SimplePage


class UserFavViewSet(
    SimplePage, viewsets.GenericViewSet, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """
    list:
        用户收藏列表
    create:
        新增收藏
    destroy:
        删除收藏
    retrieve:
        判断某个商品是否已经收藏
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        # 只获取当前用户的收藏
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        serializer_map = {
            'retrieve': UserFavDetailSerializer,
            'list': UserFavDetailSerializer,
            'create': UserFavSerializer,
            'destroy': UserFavSerializer,
        }
        return serializer_map.get(self.action, UserFavSerializer)

    def perform_create(self, serializer):
        """
        收藏数加1
        """
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


class LeavingMessageViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin,
    mixins.DestroyModelMixin, mixins.CreateModelMixin,
):
    """
    list:
        留言列表
    create:
        新增留言
    destroy:
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    """
    list:
        获取收货地址列表
    create:
        新增收货地址
    destroy:
        删除收货地址
    retrieve:
        收货地址详情
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
