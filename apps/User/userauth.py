#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from apps.User.models import User
from rest_framework.views import APIView
from django.http import JsonResponse


class UserLoginAPIView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer


class UserInfo(APIView):
    def get(self, request, *args, **kwargs):
        res = {
            "code": 20000,
            "msg": "获取用户信息成功",
            "data": []
        }
        try:
            userInfo = list(User.objects.filter(username=request.user.username).values())
            if len(userInfo) > 0:
                userInfo = userInfo[0]
            else:
                userInfo = {}
            res["data"] = userInfo
        except Exception as e:
            res["code"] = -1
            res["msg"] = f"获取用户信息失败, {e}"

        return JsonResponse(res)