import json

from django.views.generic.base import View
# from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        goods = Goods.objects.all()[:10]
        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        return JsonResponse(json_data)
