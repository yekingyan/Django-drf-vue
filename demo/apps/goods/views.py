from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    status,
    mixins,
    generics,
)

from .models import Goods
from .serializers import GoodsSerializer
# Create your views here.

from rest_framework.pagination import PageNumberPagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class GoodsListView(generics.ListAPIView,
                    generics.CreateAPIView,):
    # 将定义分页的类加入View中
    pagination_class = StandardResultsSetPagination
    # queryset 和 serializer_class 是必须的
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
