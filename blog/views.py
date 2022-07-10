# 视图层
# 与前端进行交互
# 链接前后端
from django.shortcuts import render

# Create your views here.

# 主页(未登录)


def index_unlog(request):
    return render(request, 'index_unlog.html')


def login(request):
    return render(request, 'login.html')
