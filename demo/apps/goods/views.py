from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    status,
    mixins,
    generics,
    viewsets,
)

from .models import Goods
from .serializers import GoodsSerializer
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

    def get_queryset(self):
        queryset = Goods.objects.all()
        price_min = self.request.query_params.get('price_min', 0)
        if price_min:
            queryset = queryset.filter(shop_price__gte=int(price_min))
        return queryset
