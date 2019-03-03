import django_filters
from django.db.models import Q

from .models import Goods


class GoodsFiter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    pricemin = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')
    pricemax = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    class Meta:
        model = Goods
        # 需要完成匹配的放进fields中
        fields = ['id']

    def top_category_filter(self, queryset, name, value):
        q = Q(category__id=value) \
            | Q(category__parent_category__id=value) \
            | Q(category__parent_category__parent_category__id=value)
        return queryset.filter(q)
