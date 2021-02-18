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
                print(userInfo, "uuuuuuuuuuuuuuu1111111")
                userInfo = {}
                print(userInfo, "uuuuuuuuuuuuuuu2222222")
            res["data"] = userInfo
        except Exception as e:
            res["code"] = -1
            res["msg"] = f"获取用户信息失败, {e}"

        return JsonResponse(res)

class Mylist(APIView):
    def get(self, request, *args, **kwargs):
        resstr = '''{"code":20000,"data":{"total":100,"items":[{"id":1,"timestamp":1159420361988,"author":"William","reviewer":"Anna","title":"Gepz Dyjaikzfm Fjfkt Ipnoeowrn Ndysdjupc Wvjor Lgptirgsq","content_short":"mock data","content":"<p>我是测试数据我是测试数据</p><p><img src=\"https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943\"></p>","forecast":84.61,"importance":3,"type":"EU","status":"draft","display_time":"2004-01-30 13:51:26","comment_disabled":true,"pageviews":4353,"image_uri":"https://wpimg.wallstcn.com/e4558086-631c-425c-9430-56ffb46e70b3","platforms":["a-platform"]},{"id":2,"timestamp":1426596869095,"author":"Jason","reviewer":"Sarah","title":"Mkufdeseqh Dqmtznb Ibkn Sgxf Wypbbv Tlklxiisxt Jgdntf Rkitoivjo Eopsm","content_short":"mock data","content":"<p>我是测试数据我是测试数据</p><p><img src=\"https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943\"></p>","forecast":15.12,"importance":3,"type":"EU","status":"draft","display_time":"1994-02-20 01:21:27","comment_disabled":true,"pageviews":3986,"image_uri":"https://wpimg.wallstcn.com/e4558086-631c-425c-9430-56ffb46e70b3","platforms":["a-platform"]}]}}'''
        res=json.loads(resstr)
        return JsonResponse(res)