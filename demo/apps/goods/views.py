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


class GoodsListView(generics.ListAPIView,
                    generics.CreateAPIView,):

    # queryset 和 serializer_class 是必须的
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializer

