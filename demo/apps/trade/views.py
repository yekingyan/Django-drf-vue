from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import ShoppingCart
from .serializers import ShopCartSerializer, ShopCartDetailSerializer

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
