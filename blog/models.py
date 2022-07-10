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

    def __str__(self):
        return self.username

    def comment(self):
        self.comment_num += 1
        self.save(update_fields=['comment_num'])

    def comment_del(self):
        self.comment_num -= 1
        self.save(update_fields=['comment_num'])

    class Meta:
        verbose_name = '用户'  # 指定后台显示模型名称
        verbose_name_plural = '用户'  # 指定后台显示模型复数名称
        db_table = "blog_user"  # 数据库表名


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
