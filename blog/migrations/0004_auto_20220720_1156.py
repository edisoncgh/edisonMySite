# Generated by Django 3.2.5 on 2022-07-20 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='文章分类'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content_type',
            field=models.CharField(choices=[('sm', '说说'), ('lg', '博文')], default='lg', max_length=5, verbose_name='内容类型'),
        ),
    ]
