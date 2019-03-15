from random import sample
import json

from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import SmsSerializer, UserRegisterSerializer, UserDetailSerializer
from .models import VerifyCode
from utils.yunpian import YunPian
# Create your views here.

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = '1234567890'
        code = ''.join(sample(seeds, 4))
        return code

    def create(self, request, *args, **kwargs):
        # 参数验证
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        # 发验证码
        mobile = serializer.validated_data.get('mobile')
        yun_pian = YunPian()
        code = self.generate_code()
        sms_status, msg = yun_pian.send_sms(code, mobile)

        # 返回响应
        if sms_status:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile,
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({
                'mobile': msg,
            }, status=status.HTTP_400_BAD_REQUEST, headers=headers)


class UserViewSet(CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    create:
        创建用户
    retrieve:
        用户详情
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    def get_object(self):
        """
        详情与删除只返回当前用户
        """
        """
                Returns the object the view is displaying.

                You may want to override this if you need to provide non-standard
                queryset lookups.  Eg if objects are referenced using multiple
                keyword arguments in the url conf.
        """
        return self.request.user

    def get_permissions(self):
        """
        根据行为分配不同的权限
        """
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def get_serializer_class(self):
        """
        详情与创建用不同的serializer
        """
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        serializer_action = {
            'retrieve': UserDetailSerializer,
            'create': UserRegisterSerializer,
            'update': UserDetailSerializer,
        }
        return serializer_action.get(self.action, UserDetailSerializer)

    def perform_create(self, serializer):
        """返回user(原方法没有return)"""
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 用user信息生成JWT返回
        user = self.perform_create(serializer)
        payload = jwt_payload_handler(user)
        data = serializer.data
        data['token'] = jwt_encode_handler(payload)
        data['name'] = user.name if user.name else user.username
        print(data, type(data))

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
