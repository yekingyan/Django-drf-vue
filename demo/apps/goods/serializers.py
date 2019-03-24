from django.db.models import Q

from rest_framework import serializers

from goods.models import (
    Goods,
    GoodsCategory,
    GoodsImage,
    Banner,
    GoodsCategoryBrand,
    IndexAd,
)


class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer2(serializers.ModelSerializer):
    # sub_cat 是relate_name 一对多 反查
    # 商品类别是嵌套的关系
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer(serializers.ModelSerializer):
    # sub_cat 是relate_name 一对多 反查
    # 商品类别是嵌套的关系
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    # 用序列化的category替换默认的category
    category = GoodsCategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # 指定参数， 通过Goods的models中的字段作映射
        # fields = ('name', 'add_time', 'click_num')
        # 也可以指定所有
        fields = '__all__'

    def create(self, validated_data):
        # 写入满足上面类变量的validate_data到数据库
        return Goods.objects.create(**validated_data)


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexAd
        fields = '__all__'


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    # 商品类别有三层，商品挂在最下层的类别中
    goods = serializers.SerializerMethodField()
    sub_cat = GoodsCategorySerializer2(many=True)
    indexAd = IndexAdSerializer(many=True)

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(
            Q(category_id=obj.id) | Q(category__parent_category_id=obj.id)
            | Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True)
        return goods_serializer.data

    # def get_ad_goods(self, obj):
    #     goods_json = {}
    #     ad_goods = IndexAd.objects.filter(category_id=obj.id)

    class Meta:
        model = GoodsCategory
        fields = '__all__'
