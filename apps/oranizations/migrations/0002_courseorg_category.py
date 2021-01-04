# Generated by Django 2.2.17 on 2020-12-29 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oranizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('pxjg', '培训机构'), ('gx', '高校'), ('grjg', '个人')], default='pxjg', max_length=20, verbose_name='机构类型'),
        ),
    ]