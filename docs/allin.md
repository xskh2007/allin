# allin项目，采用前后端分离模式开发
前端：Vue admin template  
后端：Django-rest-framework JWT  
参考：https://www.bilibili.com/read/cv6550664/  
https://juejin.cn/post/6844904190133665806#heading-6  
我们用 Django 和 rest-framework 开发用户模块, 并使用 JWT(Json Web Token) 进行用户认证,  
- 开发环境：centos7  
- 开发 IDE：Pycharm  
- 开发框架：Django  
- 开发语言：Python  

## 1.用Pycharm新建一个项目，用独立venv环境。
![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboard.png?raw=true)  
![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboard2.png?raw=true)  
## 2.新建一个app
### 在 allin根目录下创建应用总模块 apps：  
    cd /opt/allin/  
    mkdir apps  

### 进入 apps 创建应用模块 User, 这儿采用傻瓜式操作, 创建层级 Django-APP：  
    cd apps  
    python3 ../manage.py startapp User  
如果报错就settings.py文件加入 import os  
![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboard3.png?raw=true)  
## 3.创建数据库
    mysql> create database allin;
    Query OK, 1 row affected (0.01 sec)

## 4.修改数据库配置
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'allin',
            'USER': 'root',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    } 
     
![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboard4.png?raw=true)   
## 安装mysql客户端库      
    pip install mysqlclient

最后
    cd apps
    python3 ../manage.py startapp User
此时项目结构如下：

![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboard5.png?raw=true)   

## 5.修改配置：
修改 apps/User/apps.py：  

    from django.apps import AppConfig  


    class UserConfig(AppConfig):
    
## 6.添加 allin/settings.py 中应用注册参数 INSTALLED_APPS：

    INSTALLED_APPS = [
        ...,
        'apps.User',
    ]  

![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboard6.png?raw=true)   

## 7.在 allin/setting.py 中修改配置时区参数 TIME_ZONE:
    TIME_ZONE = 'Asia/Shanghai'

## 8.在 allin/setting.py 中修改配置时区参数 ALLOWED_HOSTS :
    ALLOWED_HOSTS = ["*"]

## 9.启动项目
    python3 manage.py runserver 0.0.0.0:8000  

![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboard7.png?raw=true)   

![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboard8.png?raw=true)

## 10.创建 User 模型
在 apps/User/models.py 中自定义我们的用户模型类  
    from django.contrib.auth.models import AbstractUser


    class User(AbstractUser):
        class Meta:
            db_table = 'allin_user'
            ordering = ('-id',)
我们采用的是继承 AbstractUser 类并指定 db_table 的方式, 此时你可以使用 Pycharm 的 Ctrl + B 进入父类中查看 User 具有的属性和方法。  
当然了, 在执行到这个步骤的时候其实用户的模型类并没有生效, 而需要达到生效的效果则是需要指定用户模型类的位置参数, 你只需要在 allin/settings.py 中用 AppName.UserModelsName 的方式指定用户模型类即可：  

    AUTH_USER_MODEL = 'User.User'  

有关于用户认证的模型类介绍, 推荐你查阅 Customizing authentication in Django。
使用 Django 迁移命令迁移数据库生成数据表：  
    python3 manage.py makemigrations
    python3 manage.py migrate

你可以使用 MySQL 数据库连接应用查看你生成的数据表。

![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboard9.png?raw=true)


## 登录认证
    pip install djangorestframework-jwt
    pip install djangorestframework

### 在准备好基本环境后我们进行登录接口的开发工作, 登录的接口主要是对用户进行验证以及口令的返回, 使用 JWT 验证的时候先安装导入需要的包应用 rest_framework, 添加 Medusa/settings.py 中应用注册参数 INSTALLED_APPS：
    INSTALLED_APPS = [
        ...,
        'rest_framework',
    ]
### 在 apps/User/ 下创建用户认证的视图文件 userauth.py 并撰写用户登录认证视图类：
    #!/usr/bin/env python
    # _*_ Coding: UTF-8 _*_
    from rest_framework_jwt.serializers import JSONWebTokenSerializer
    from rest_framework_jwt.views import JSONWebTokenAPIView
    
    
    class UserLoginAPIView(JSONWebTokenAPIView):
        serializer_class = JSONWebTokenSerializer
### 简简单单的几行代码就实现了一个用户登录的接口, 你现在就需要在你的路由管理器里面注册这个登录的 API 试图即可, 在 allin/urls.py 中 urlpatterns 参数中注册路由：
    urlpatterns = [
        path('api/v1.0.0/user/login', userauth.UserLoginAPIView.as_view())
    ]


不要着急, 我们是不是还没有创建用户呢？  

    python3 manage.py createsuperuser

### 用户信息接口  
## 在 apps/User/ 下创建用户认证的视图文件 userauth.py 并撰写用户登录认证视图类：
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

## 在 allin/urls.py 中 urlpatterns 参数中注册路由：

    from apps.User import userauth #引入userauth 
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/v1.0.0/user/login', userauth.UserLoginAPIView.as_view()),
        path('api/v1.0.0/user/userinfo', userauth.UserInfo.as_view())
    ]

postman测试
http://127.0.0.1:8000/api/v1.0.0/user/login

![GitHub](https://github.com/xskh2007/allin/blob/main/docs/imgs/clipboar10d.png?raw=true)