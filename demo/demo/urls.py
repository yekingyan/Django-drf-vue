"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from .settings import MEDIA_ROOT

# from goods.views_base import GoodsListView
from goods.views import (
    GoodsListViewSet,
    GoodsCategoryViewSet,
    BannerViewSet,
    IndexCategoryViewSet,
)
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import (
    UserFavViewSet, LeavingMessageViewSet,
    AddressViewSet,
)
from trade.views import ShoppingCartViewSet, OrderViewSet

router = DefaultRouter()

# 商品列表
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 商品类别列表
router.register(r'categorys', GoodsCategoryViewSet, base_name='categorys')
# 轮播图
router.register(r'banners', BannerViewSet, base_name='banners')
# 首页商品系列数据
router.register(r'indexGoods', IndexCategoryViewSet, base_name='indexGoods')

# 验证码
router.register(r'codes', SmsCodeViewSet, base_name='codes')
# 用户注册
router.register(r'users', UserViewSet, base_name='users')

# 用户收藏
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
# 用户留言
router.register(r'messages', LeavingMessageViewSet, base_name='messages')
# 收货地址
router.register(r'address', AddressViewSet, base_name='address')

# 购物车
router.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')
# 订单
router.register(r'orders', OrderViewSet, base_name='orders')

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 商品列表页
    # url(r'goods/$', goods_list, name='goods-list'),

    url(r'^', include(router.urls)),

    url(r'^docs/', include_docs_urls(title='项目文档')),

    # drf 自带的token认证模式
    url(r'api-token-auth/', views.obtain_auth_token),

    # jwt的token认证模式
    url(r'^login/', obtain_jwt_token),
]
