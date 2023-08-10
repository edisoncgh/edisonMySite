# 表单类
# 主要用来实现评论区
from django import forms
from mdeditor.fields import MDTextFormField
from captcha.fields import CaptchaField
from .models import Comment


class CommentForm(forms.Form):
    nickname = forms.CharField(max_length=20, label='你的昵称')
    author_email = forms.EmailField(label='你的邮箱')
    author_link = forms.URLField(
        label='你的链接', required=False)  # 非必需字段
    comment_content = MDTextFormField(label='评论内容')
    captcha = CaptchaField(label='验证码')
    article_id = forms.IntegerField()  # 所属文章id

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if not nickname:
            raise forms.ValidationError("请输入昵称")
        return nickname

    def clean_author_email(self):
        author_email = self.cleaned_data.get('author_email')
        if not author_email:
            raise forms.ValidationError("请输入邮箱")
        return author_email

    def clean_author_link(self):
        author_link = self.cleaned_data.get('author_link')
        # 在这里添加自定义的链接验证逻辑
        return author_link

    # 更多的clean方法...

    def clean(self):
        cleaned_data = super().clean()
        # 在这里执行任何整体表单级别的验证逻辑
        return cleaned_data
