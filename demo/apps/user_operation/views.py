from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


from .models import UserFav
from .serializers import UserFavSerializer
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
        收藏详情
    """
    serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        # 只获取当前用户的收藏
        return UserFav.objects.filter(user=self.request.user)


