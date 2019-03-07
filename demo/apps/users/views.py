from random import sample
import json

from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import SmsSerializer, UserRegisterSerializer
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


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()