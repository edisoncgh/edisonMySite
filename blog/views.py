# 视图层
# 与前端进行交互
# 链接前后端
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.mail import send_mail  # 邮件推送
from django.shortcuts import redirect, reverse
from .models import Article, Comment, Category
from .forms import CommentForm
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
    article = get_object_or_404(Article, pk=article_id)  # 获取文章
    article.visited()
    comments = Comment.objects.filter(article=article_id)  # 获取评论列表
    category = get_object_or_404(Category, pk=article.category.cat_id)  # 获取分类

    # 获取前一篇与后一篇文章
    previous_post = Article.objects.filter(article_id=article_id-1)
    if previous_post and id != 0:
        previous_post = Article.objects.get(article_id=article_id-1)
    next_post = Article.objects.filter(article_id=article_id+1)
    if next_post:
        next_post = Article.objects.get(article_id=article_id+1)

    return render(request, 'articles/article_content.html', {'article': article, 'comments': comments, 'prevpost': previous_post, 'nextpost': next_post, 'category': category})


def article_list(request):  # 文章列表
    try:
        article_list = Article.objects.order_by('-publish_date')
        context = {'article_list': article_list}
    except Article.DoesNotExist:
        raise Http404("这里还没有文章喔")
    return render(request, 'index_unlog.html', context)

# def submit_comment(request):  # 提交评论
#     if request.method == "POST":
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             article_id = form.cleaned_data['article_id']
#             article = get_object_or_404(Article, pk=article_id)
#             comment = Comment(
#                 article=article,
#                 content=form.cleaned_data['comment_content'],
#                 author=form.cleaned_data['nickname'],
#                 author_email=form.cleaned_data['author_email'],
#                 author_link=form.cleaned_data['author_link']
#             )
#             comment.save()

#             # 动态生成url
#             url = reverse('blog:content', args=[article_id])
#             return redirect(url)

#     # 如果表单验证失败，或者不是POST请求，返回到原页面或其他逻辑
#     return render(request, 'articles/article_content.html', {"commentForm": form})


def submit_comment(request):  # 提交评论
    if request.method == "POST":
        # 从post中获取内容
        article_id = request.POST.get('article_id')
        nickname = request.POST.get('nickname')
        author_email = request.POST.get('author_email')
        author_link = request.POST.get('author_link')
        comment_content = request.POST.get('comment_content')
        # 动态生成url
        url = reverse('blog:content', args=[article_id])
        # 创建评论对象并保存到数据库
        article = get_object_or_404(Article, pk=article_id)
        comment = Comment(
            article=article, content=comment_content,
            author=nickname, author_email=author_email, author_link=author_link
        )
        comment.save()

    return redirect(url)


def archive(request):  # 归档页面
    articles = Article.objects.filter(
        publish_date__isnull=False
    ).order_by('-publish_date')

    return render(request, 'archive.html', {'articles': articles})


def category_articles(request, category_id):  # 分类页面
    category = Category.objects.get(cat_id=category_id)
    articles = Article.objects.filter(
        category=category
    ).order_by('-publish_date')

    context = {
        'category': category,
        'articles': articles,
    }

    return render(request, 'category.html', context)
