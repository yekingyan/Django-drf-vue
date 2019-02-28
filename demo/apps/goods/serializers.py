from rest_framework import serializers

from goods.models import Goods, GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    # 用序列化的category替换默认的category
    category = CategorySerializer()

    class Meta:
        model = Goods
        # 指定参数， 通过Goods的models中的字段作映射
        # fields = ('name', 'add_time', 'click_num')
        # 也可以指定所有
        fields = '__all__'

    def create(self, validated_data):
        # 写入满足上面类变量的validate_data到数据库
        return Goods.objects.create(**validated_data)
