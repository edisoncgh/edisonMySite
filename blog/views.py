# 视图层
# 与前端进行交互
# 链接前后端
from django.shortcuts import render, get_object_or_404
from .models import Article, Comment
# Create your views here.


def start_page(request):  # 起始页
    return render(request, 'start_page.html')


def index_unlog(request):  # 博客主页
    try:
        article_list = Article.objects.order_by('-publish_date')
        context = {'article_list': article_list}
    except Article.DoesNotExist:
        raise Http404("这里还没有文章喔")
    return render(request, 'index_unlog.html', context)


def login(request):  # 博客登录页
    return render(request, 'login.html')


def article_content(request, article_id):  # 文章详情
    article = get_object_or_404(Article, pk=article_id)  # 获取文章列表
    comments = Comment.objects.filter(article=article_id)  # 获取评论列表

    # 获取前一篇与后一篇文章
    previous_post = Article.objects.filter(article_id=article_id-1)
    if previous_post and id != 0:
        previous_post = Article.objects.get(article_id=article_id-1)
    next_post = Article.objects.filter(article_id=article_id+1)
    if next_post:
        next_post = Article.objects.get(article_id=article_id+1)

    return render(request, 'articles/article_content.html', {'article': article, 'comments': comments, 'prevpost': previous_post, 'nextpost': next_post})


def article_list(request):  # 文章列表
    try:
        article_list = Article.objects.order_by('-publish_date')
        context = {'article_list': article_list}
    except Article.DoesNotExist:
        raise Http404("这里还没有文章喔")
    return render(request, 'index_unlog.html', context)
