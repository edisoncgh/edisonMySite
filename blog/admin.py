# 系统后台
from django.contrib import admin

from .models import Article, Category, Comment, Friendlink
# Register your models here.
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Friendlink)
