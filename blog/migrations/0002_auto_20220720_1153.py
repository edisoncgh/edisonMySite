# Generated by Django 3.2.5 on 2022-07-20 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-publish_date'], 'verbose_name': '文章', 'verbose_name_plural': '所有文章'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '类别', 'verbose_name_plural': '所有类别'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-comment_date'], 'verbose_name': '评论', 'verbose_name_plural': '所有评论'},
        ),
        migrations.AlterModelOptions(
            name='friendlink',
            options={'verbose_name': '友链', 'verbose_name_plural': '所有友链'},
        ),
        migrations.AddField(
            model_name='article',
            name='content_type',
            field=models.CharField(choices=[('sm', '说说'), ('lg', '博文')], default='lg', max_length=5),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(default='无题', max_length=50, verbose_name='标题'),
        ),
    ]