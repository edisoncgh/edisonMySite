from django.urls import path

from . import views

urlpatterns = [
    # 博客子系统默认页面路由
    path('', views.index_unlog, name='index_unlog'),
    # 博客子系统登录界面路由
    path('login', views.login, name='login'),
]
