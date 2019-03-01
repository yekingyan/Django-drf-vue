from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    status,
    mixins,
    generics,
    viewsets,
)
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods
from .serializers import GoodsSerializer
from .filters import GoodsFiter
# Create your views here.


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     page_query_param = 'p'
#     max_page_size = 100


class GoodsListViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 设置filter
    filter_backends = (DjangoFilterBackend,)
    filter_class = GoodsFiter

