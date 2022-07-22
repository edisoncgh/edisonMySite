"""edisonContentManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# 全局路由
# 配置页面跳转信息
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog import views

urlpatterns = [
    # 配置缺省页面
    path('', views.start_page, name='start_page.html'),
    # 配置管理页面路由
    path('admin/', admin.site.urls),
    # 配置博客子系统路由
    path('blog/', include('blog.urls')),
    # 验证码生成器
    path('captcha/', include('captcha.urls')),
]
