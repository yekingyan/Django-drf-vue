from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Goods
from .serializers import GoodsSerializer
# Create your views here.


class GoodsListView(APIView):

    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)
