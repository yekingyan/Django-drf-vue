from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    status,
    mixins,
    generics,
    viewsets,
    filters,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import (
    Goods,
    GoodsCategory,
    Banner,
)
from .serializers import (
    GoodsSerializer,
    GoodsCategorySerializer,
    BannerSerializer,
    IndexCategorySerializer,
)
from .filters import GoodsFiter
# Create your views here.


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     page_query_param = 'p'
#     max_page_size = 100


class GoodsListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    list:
        商品列表
    retrieve:
        商品详情
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 设置filter，django-filter过滤，DRF的filter搜索
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFiter
    # 一个字段搜下面的所有参数，注意和filter区别
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 排序设置, 需要入参{'ordering': '-add_time'}
    ordering_fields = ('add_time', 'shop_price', 'sold_num')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 加入点击数纪录
        instance.click_num += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsCategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    list:
        商品分类列表数据
    retrieve:
        商品分类详情
    """
    # 获取第一类
    queryset = GoodsCategory.objects.filter(category_type=1).select_related()
    serializer_class = GoodsCategorySerializer

    # 虽然支持jwt + token，但单个接口可在这里规定只支持jwt
    authentication_classes = (JSONWebTokenAuthentication,)
    # permission作权限限制
    permission_classes = (IsAuthenticated,)


# class HotSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     """
#     list:
#         获取热搜词列表
#     """
#     queryset =

class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    serializer_class = BannerSerializer
    queryset = Banner.objects.all().order_by('index')


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        首页商品分页数据列表
    """
    serializer_class = IndexCategorySerializer
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '酒水饮料'])
