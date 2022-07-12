# 实体层
# 对应数据库
from django.db import models
import datetime
from django.contrib import admin

# Create your models here.

# ---------------------------用户表---------------------------


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    created_time = models.CharField(
        max_length=50, default=datetime.datetime.now().strftime('%Y-%m-%d'))  # 创建时间
    comment_num = models.PositiveIntegerField(
        verbose_name='评论数', default=0)  # 评论数
    avatar = models.ImageField(
        upload_to='media', default="media/default.jpg")  # 用户头像

    @classmethod
    def __str__(self):
        return self.username

    @classmethod
    def comment(self):
        self.comment_num += 1
        self.save(update_fields=['comment_num'])

    @classmethod
    def comment_del(self):
        self.comment_num -= 1
        self.save(update_fields=['comment_num'])

    # 模型元数据选项
    class Meta:
        verbose_name = '用户'  # 指定后台显示模型名称
        verbose_name_plural = '用户'  # 指定后台显示模型复数名称
        db_table = "blog_user"  # 数据库表名


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

# ---------------------------文章表---------------------------


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '已发表'),
    )
    article_id = models.IntegerField(
        verbose_name='文章ID', primary_key=True)  # 主键，自增
    article_cat = models.CharField(
        verbose_name='文章分类', max_length=20)
    title = models.CharField(verbose_name='标题', max_length=50)
    content = models.TextField(verbose_name='正文', blank=True, null=True)
    publish_date = models.DateTimeField(
        verbose_name='发布日期', default=datetime.datetime.now().strftime('%Y-%m-%d'))
    comment_num = models.PositiveIntegerField(verbose_name='评论数', default=0)
    like_num = models.PositiveIntegerField(verbose_name='点赞数', default=0)
    visit_num = models.PositiveIntegerField(verbose_name='浏览数', default=0)

    # 使对象在后台显示更友好
    @classmethod
    def __str__(self):
        return self.title

    # 更新浏览量
    @classmethod
    def visited(self):
        self.visit_num += 1
        self.save(update_fields=['visit_num'])

    # 下一篇
    @classmethod
    def next_article(self):  # id比当前id大，状态为已发布，发布时间不为空
        return Article.objects.filter(id__gt=self.article_id, status='p', pub_time__isnull=False).first()

    # 前一篇
    @classmethod
    def prev_article(self):  # id比当前id小，状态为已发布，发布时间不为空
        return Article.objects.filter(id__lt=self.article_id, status='p', pub_time__isnull=False).first()

    # 模型元数据选项
    class Meta:
        db_table = "articles"  # 数据库表名
        ordering = ['-publish_date']  # 按发布日志降序排序
# ---------------------------分类表---------------------------


class Category(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # 外键，指向所属文章
    cat_id = models.IntegerField(
        verbose_name='类别ID', primary_key=True)  # 主键，自增
    cat_name = models.CharField(
        verbose_name='类别名称', max_length=20)

    @classmethod
    # 使对象在后台显示更友好
    def __str__(self):
        return self.cat_name

    # 模型元数据选项
    class Meta:
        db_table = "categories"  # 数据库表名

# ---------------------------评论表---------------------------


class Comment(models.Model):
    STATUS_CHOICES = (
        ('f', '待通过'),
        ('t', '已通过'),
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # 外键，指向所属文章
    comment_id = models.IntegerField(
        verbose_name='评论ID', primary_key=True)  # 主键，自增
    author = models.CharField(
        verbose_name='评论作者', max_length=20)
    author_email = models.EmailField(
        verbose_name='作者邮箱')
    author_link = models.URLField(
        verbose_name='作者链接', default='')
    comment_date = models.DateTimeField(
        verbose_name='评论日期', default=datetime.datetime.now())
    content = models.TextField(verbose_name='评论正文', blank=True, null=True)

    @classmethod
    # 使对象在后台显示更友好
    def __str__(self):
        return self.content

    # 模型元数据选项
    class Meta:
        db_table = "comments"  # 数据库表名
        ordering = ['-comment_date']  # 按发布日志降序排序
# ---------------------------友链表---------------------------


class Friendlink(models.Model):
    link_id = models.IntegerField(
        verbose_name='友链ID', primary_key=True)  # 主键，自增
    link_url = models.URLField(
        verbose_name='友链地址')
    link_desc = models.CharField(
        verbose_name='友链描述', max_length=100)
    link_name = models.CharField(
        verbose_name='友链名称', max_length=20)
    link_avatar = models.ImageField(
        verbose_name='友链头像', upload_to='media', default="media/default.jpg")

    @classmethod
    # 使对象在后台显示更友好
    def __str__(self):
        return self.link_name

    # 模型元数据选项
    class Meta:
        db_table = "friendlinks"  # 数据库表名
