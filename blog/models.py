# 实体层
# 对应数据库
import hashlib  # 哈希库
from django.db import models
from django.utils import timezone
from django.contrib import admin
from mdeditor.fields import MDTextField

# Create your models here.

# ---------------------------用户表---------------------------


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    created_time = models.CharField(
        max_length=50, default=timezone.now)  # 创建时间
    comment_num = models.PositiveIntegerField(
        verbose_name='评论数', default=0)  # 评论数
    avatar = models.ImageField(
        upload_to='media', default="media/default.jpg")  # 用户头像

    def __str__(self):
        return self.username

    def comment(self):
        self.comment_num += 1
        self.save(update_fields=['comment_num'])

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

# ---------------------------分类表---------------------------


class Category(models.Model):
    cat_id = models.AutoField(verbose_name='类别id', primary_key=True)  # 主键，自增
    cat_name = models.CharField(
        verbose_name='类别名称', max_length=20, null=False)
    add_date = models.DateTimeField(
        verbose_name='添加日期', default=timezone.now)

    # 使对象在后台显示更友好
    def __str__(self):
        if self.cat_name:
            return self.cat_name
        else:
            return "empty field"

    # 模型元数据选项
    class Meta:
        db_table = "categories"  # 数据库表名
        verbose_name = '类别'  # 指定后台显示模型名称
        verbose_name_plural = '所有类别'  # 指定后台显示模型复数名称

# ---------------------------文章表---------------------------


class Article(models.Model):
    SMALL_TALK = 'sm'
    BLOG_ARTICLE = 'lg'
    CONTENT_TYPE_CHOICE = (
        (SMALL_TALK, '说说'),
        (BLOG_ARTICLE, '博文')
    )

    content_type = models.CharField(
        max_length=5,
        choices=CONTENT_TYPE_CHOICE,
        default=BLOG_ARTICLE,
        verbose_name='内容类型'
    )  # 内容类型，默认为博文
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='文章分类', null=True, blank=True)  # 外键，指向所属分类
    article_id = models.IntegerField(
        verbose_name='文章ID', primary_key=True)  # 主键，自增
    title = models.CharField(verbose_name='标题', max_length=50, default='无题')
    content = MDTextField(verbose_name='正文', blank=True, null=True)
    publish_date = models.DateTimeField(
        verbose_name='发布日期', default=timezone.now, editable=False)
    comment_num = models.PositiveIntegerField(
        verbose_name='评论数', default=0, editable=False)
    like_num = models.PositiveIntegerField(
        verbose_name='点赞数', default=0, editable=False)
    visit_num = models.PositiveIntegerField(
        verbose_name='浏览数', default=0, editable=False)

    # 使对象在后台显示更友好
    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'empty'

    # 更新浏览量
    def visited(self):
        self.visit_num += 1
        self.save(update_fields=['visit_num'])

    # 更新点赞
    def liked(self):
        self.like_num += 1
        self.save(update_fields=['like_num'])

    # 下一篇
    def next_article(self):  # id比当前id大，状态为已发布，发布时间不为空
        return Article.objects.filter(id__gt=self.article_id, pub_time__isnull=False).first()

    # 前一篇
    def prev_article(self):  # id比当前id小，状态为已发布，发布时间不为空
        return Article.objects.filter(id__lt=self.article_id, pub_time__isnull=False).first()

    # 模型元数据选项
    class Meta:
        db_table = "articles"  # 数据库表名
        ordering = ['-publish_date']  # 按发布日志降序排序
        verbose_name = '文章'  # 指定后台显示模型名称
        verbose_name_plural = '所有文章'  # 指定后台显示模型复数名称


# ---------------------------评论表---------------------------


class Comment(models.Model):
    PERMIT = 'per'
    NOT_PERMIT = 'npr'
    STATUS_CHOICES = (
        (PERMIT, '已通过'),
        (NOT_PERMIT, '未通过'),
    )

    status = models.CharField(
        max_length=5,
        choices=STATUS_CHOICES,
        default=NOT_PERMIT,
        verbose_name='评论状态'
    )  # 评论状态，默认不过审
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=False)  # 外键，指向所属文章
    comment_id = models.AutoField(
        verbose_name='评论ID', primary_key=True)  # 主键，自增
    author = models.CharField(
        verbose_name='评论作者', max_length=20)
    author_email = models.EmailField(
        verbose_name='作者邮箱')
    author_link = models.URLField(
        verbose_name='作者链接', default='', null=True, blank=True)
    comment_date = models.DateTimeField(
        verbose_name='评论日期', default=timezone.now)
    content = MDTextField(verbose_name='评论正文', null=True)  # markdown内容

    def __str__(self):
        if self.author:
            return self.author
        else:
            return "empty field"

    def get_gravatar(self, size=80):
        email_hash = hashlib.md5(
            self.author_email.lower().encode('utf-8')).hexdigest()
        gravatar_url = f"https://cdn.v2ex.com/gravatar/{email_hash}?s={size}&d=identicon"
        return gravatar_url

    class Meta:
        db_table = "comments"  # 数据库表名
        ordering = ['-comment_date']  # 按发布日志降序排序
        verbose_name = '评论'  # 指定后台显示模型名称
        verbose_name_plural = '所有评论'  # 指定后台显示模型复数名称

# ---------------------------楼中楼---------------------------


class Subcomment(models.Model):
    father = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=False)  # 父评论
    id = models.AutoField(
        verbose_name='子评论ID', primary_key=True)  # 主键，自增
    author = models.CharField(
        verbose_name='子评论作者', max_length=20)
    author_email = models.EmailField(
        verbose_name='作者邮箱')
    author_link = models.URLField(
        verbose_name='作者链接', default='', null=True, blank=True)
    comment_date = models.DateTimeField(
        verbose_name='评论日期', default=timezone.now)
    content = MDTextField(verbose_name='子评论正文', null=True)  # markdown内容

    def __str__(self):
        if self.author:
            return self.author
        else:
            return "empty field"

    class Meta:
        db_table = "subcomments"  # 数据库表名
        ordering = ['-comment_date']  # 按发布日志降序排序
        verbose_name = '子评论'  # 指定后台显示模型名称
        verbose_name_plural = '所有子评论'  # 指定后台显示模型复数名称
# ---------------------------友链表---------------------------


class Friendlink(models.Model):
    link_id = models.AutoField(
        verbose_name='友链ID', primary_key=True)  # 主键，自增
    link_url = models.URLField(
        verbose_name='友链地址')
    link_desc = models.CharField(
        verbose_name='友链描述', max_length=100)
    link_name = models.CharField(
        verbose_name='友链名称', max_length=20)
    # 图片会被上传至MEDIA_ROOT / uploads
    # MEDIA_ROOT = BASE_DIR / blog / static / media
    link_avatar = models.ImageField(
        verbose_name='友链头像',
        upload_to='uploads/',  # 媒体文件路径会添加到 MEDIA_ROOT 下
        default="default.jpg"  # 默认图片路径相对于 upload_to
    )

    # 使对象在后台显示更友好
    def __str__(self):
        if self.link_name:
            return self.link_name
        else:
            return 'empty'

    # 模型元数据选项
    class Meta:
        db_table = "friendlinks"  # 数据库表名
        verbose_name = '友链'  # 指定后台显示模型名称
        verbose_name_plural = '所有友链'  # 指定后台显示模型复数名称
