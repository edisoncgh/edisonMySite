# 表单类
# 主要用来实现评论区
from django import forms
from mdeditor.fields import MDTextFormField
from captcha.fields import CaptchaField
from .models import Comment


class CommentForm(forms.Form):
    nickname = forms.CharField(max_length=20, label='你的昵称')
    author_email = forms.EmailField(label='你的邮箱')
    author_link = url = forms.URLField(
        label='你的链接', required=False)  # 非必需字段
    comment_content = MDTextFormField(label='评论内容')
    # 验证码字段
    captcha = CaptchaField(label='验证码')
    article_id = forms.IntegerField()  # 所属文章id

    class Meta:
        model = Comment
        fields = ['author', 'content', 'author_email', 'author_link']
