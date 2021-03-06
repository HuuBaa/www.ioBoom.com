# Generated by Django 2.0.7 on 2018-08-13 10:08

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcomment',
            name='article',
            field=models.ForeignKey(help_text='从属文章', on_delete=django.db.models.deletion.CASCADE, related_name='sub_comments', to='article.Article', verbose_name='从属文章'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=20, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
