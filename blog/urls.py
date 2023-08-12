from django.urls import path
from django.conf.urls import url, include

from . import views

# 为 URL 名称添加命名空间
app_name = 'blog'
urlpatterns = [
    # 博客子系统默认页面路由
    # ex: blog/
    path('', views.index_unlog, name='index_unlog'),
    # 博客子系统登录界面路由
    # ex: blog/login
    path('login', views.login, name='login'),
    # 文章详情页路由
    # ex: blog/1/
    path('<int:article_id>/', views.article_content, name='content'),
    # 评论表单推送路由
    # ex: blog/commentpost?nickname=xxx
    path('submit_comment', views.submit_comment, name='submit_comment'),
    # 验证码路由
    path('captcha/', include('captcha.urls')),
    url("^captcha/", include('captcha.urls')),
    # 归档页面路由
    path('archive/', views.archive, name='archive'),
]
