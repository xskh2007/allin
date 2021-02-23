#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from apps.User.models import User
from rest_framework.views import APIView
from django.http import JsonResponse
import json

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
            print(request.user,"useruseruser")
            userInfo = list(User.objects.filter(username=request.user.username).values())
            if len(userInfo) > 0:
                userInfo = userInfo[0]
                print(userInfo,"uuuuuuuuuuuuuuu000000")
            else:
                # print(userInfo, "uuuuuuuuuuuuuuu1111111")
                userInfo = {}
                # print(userInfo, "uuuuuuuuuuuuuuu2222222")
            res["data"] = userInfo
        except Exception as e:
            res["code"] = -1
            res["msg"] = f"获取用户信息失败, {e}"

        return JsonResponse(res)

class Mylist(APIView):
    def get(self, request, *args, **kwargs):
        data={}
        res = {
            "code": 20000,
            "data": {}
        }
        items = list(User.objects.filter(username=request.user.username).values())
        data["total"]=1
        data["items"]=items
        res["data"] = data
        return JsonResponse(res)